# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from opaque_keys.edx.keys import CourseKey

from edxmako.shortcuts import render_to_response
from student.auth import has_course_author_access

from openedx.features.scos.conf import ENV, set_environment

from openedx.features.scos.roo import get_course_scos_id, get_course_moderation_status, get_course_scos_data, post_course_data, change_course_status, put_course_data

from openedx.features.scos.courses import upate_course_scos_data

from openedx.features.scos.portfolio import enroll_scos_user
from openedx.features.scos.users import get_user_scos_id

from django.conf import settings
from pytz import UTC

from django.contrib.auth.models import User
from xmodule.modulestore.django import modulestore

log = logging.getLogger(__name__)


@ensure_csrf_cookie
@login_required
def export_scos(request, course_key_string):
    course_key = CourseKey.from_string(course_key_string)
    course_module = modulestore().get_course(course_key)
    source_students = User.objects.filter(courseenrollment__course_id=course_key)
    #     course_key_string = 'course-v1:fa+digitalmarket+2022_os'
    #     course_key_string = 'course-v1:fa+mairbs+2022_os'
    status = 'bad settings'
    msg = ""
    current_env = ENV('DOMAIN')
    failed = False  
    
    if not has_course_author_access(request.user, course_key):
        raise PermissionDenied()              

    try:
        data = get_course_scos_data(course_key_string)
        if get_course_scos_id(course_key_string) is None:
            status = 'is_new_course'
            general_uid = False
        else:
            status = 'exist in scos'
            general_uid = get_course_scos_id(course_key_string)
    except:
        failed = True
        msg = 'Please check variables for None in ' + 'http://studio.localhost/settings/advanced/' + course_key_string
    
     
         
    if 'action' in request.GET:
        if request.GET['action'] == 'tolms':
            try:
                upate_course_scos_data(course_key_string, data)
                msg = _('passport created')
                
            except Exception as e:
                failed = True
                msg = 'Failed  with error: '+str(e)  
        elif request.GET['action'] == 'push':
            try:
                if general_uid:
                    put_course_data(data)
                    msg = _('Course successfully updated in scos repository')
                else:
                    general_uid = post_course_data(data)
                    course_module.giturl = general_uid
                    modulestore().update_item(course_module, request.user.id)
                    msg = _('New issue successfully created in scos')
            except Exception as e:
                failed = True
                msg = 'Failed  '+course_key_string + ' with error: '+str(e)
        elif request.GET['action'] == 'active':
            try:
                status = change_course_status(course_key_string, 'active')
                assert status == 'ACTIVE'
            except Exception as e:
                failed = True
                msg = 'Failed  '+status + ' with error: '+str(e) +' because status '+get_course_moderation_status(course_key_string) 
        elif request.GET['action'] == 'archive':
            try:
                status = change_course_status(course_key_string, 'archive')
                assert status == 'ARCHIVE'  
            except Exception as e:
                failed = True
                msg = 'Failed  '+status + ' with error: '+str(e) +' because status '+get_course_moderation_status(course_key_string)
        elif request.GET['action'] == 'enroll':
            try:
                for uid in source_students:
                    if get_user_scos_id(uid.id):
                        enroll_scos_user(course_key_string, uid.id)                     
                msg =  _('Users enrolled')    
            except Exception as e:
                failed = True
                msg = 'Failed  with error: '+str(e)    
        
    return render_to_response('export_scos.html', {
        'context_course': course_module,
        'msg': msg,
        'failed': failed,
        'status': status,
        'current_env': current_env
    })