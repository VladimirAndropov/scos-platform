# -*- coding: utf-8 -*-
import sys
import requests
import json
import exceptions

from openedx.features.scos.conf import ENV, HTTP_TIMEOUT, TESTING, DEBUG_OUTPUT_FILE, SSL_KEY, SSL_CERT
from openedx.features.scos.lib import ServerSession, ImpatientHTTPAdapter ,JSON_HEADER, write_json, logit
from django.utils.translation import ugettext as _
from opaque_keys.edx.keys import CourseKey
from lms.djangoapps.certificates.api import has_any_active_web_certificate
import sys
import os
import io
import json
import exceptions
import datetime
import json

from django.conf import settings
from pytz import UTC

from cms.djangoapps.models.settings.encoder import CourseSettingsEncoder
from openedx.core.djangoapps.models.course_details import CourseDetails
from django.contrib.auth.models import User
from xmodule.modulestore.django import modulestore
import datetime

api = None

def get_api_requester():
    session = ServerSession(ENV('API_URL'))
    session.auth = (ENV('API_USER'), ENV('API_PASSWORD'))
    session.mount('http://', ImpatientHTTPAdapter(HTTP_TIMEOUT))
    session.mount('https://', ImpatientHTTPAdapter(HTTP_TIMEOUT))
    return session


# def get_api_requester():
#     session = requests.Session()
#     url = "https://test.online.edu.ru/api/v1/connection/check"
#     session.get(url,  headers=JSON_HEADER, cert=(SSL_CERT, SSL_KEY))
#     # session.mount('http://', ImpatientHTTPAdapter(HTTP_TIMEOUT))
#     # session.mount('https://', ImpatientHTTPAdapter(HTTP_TIMEOUT))
#     return session


def post_course_data(data):
    # """Send new course metadata to ROO"""
    global api
    if api is None:
        api = get_api_requester()
    # url = 'v2/registry/courses' 
    url = 'courses/v0/course' 
    # url = 'https://test.online.edu.ru/api/courses/v0/course' 
    resp = api.post(url, json = json.dumps(data), headers = JSON_HEADER)
    return resp


def put_course_data(data):
    # """Send old course metadata to ROO"""
    global api
    if api is None:
        api = get_api_requester()
    url = 'courses/v0/course' 
    # url = 'v2/registry/courses' 
    resp = api.put(url, json=data, headers = JSON_HEADER)
    return resp.status_code
    
    

    
    
def get_course_moderation_status(cid):
    # """Get course moderation status from ROO"""
    global api
    data = get_course_scos_data(cid)
    scos_id = data['package']['items'][0]['id']
    if api is None:
        api = get_api_requester()
    url = 'courses/v0/get_moderation_status?course_id='
    # url = 'https://test.online.edu.ru/api/courses/v0/get_moderation_status?course_id='
    resp = api.get(url + scos_id)
    # resp = api.get(url + scos_id, data=json.dumps(payload),  headers=headers, cert=(SSL_CERT, SSL_KEY))
    print(resp.text)
    resp.raise_for_status()
    resp_data = resp.json()
    if not resp_data['status']:
        raise exceptions.RuntimeError('Unexpected error occured'
                                      + ' when trying to get moderation status')
    print('SCOS course moderation status:', resp_data['status'])
    return resp_data['status']


def change_course_status(cid, status):
    # """Change course status (active/archive) at ROO"""
    global api
    if status not in ('active', 'archive'):
        raise exceptions.RuntimeError('Unrecognized status: ' + status)
    data = get_course_scos_data(cid)
    scos_id = data['package']['items'][0]['id']
    if api is None:
        api = get_api_requester()
    url = 'courses/v0/update_status?course_id=' + scos_id + '&new_status=' + status   
    # url = 'https://test.online.edu.ru/api/courses/v0/update_status?course_id=' + scos_id + '&new_status=' + status
    resp = api.put(url)
    print(resp.text)
    resp.raise_for_status()
    resp_data = resp.json()
    if not resp_data['status']:
        sys.exit('Unexpected error occured when trying to get '
                 + 'SCOS course state for course ' + cid)
    print('New SCOS course state:', resp_data['status'])
    return resp_data['status']


def get_widget_data(course_id):
    global api
    data = get_course_scos_data(course_id)
    version = data['package']['items'][0]['business_version']    
    url = 'https://test.online.edu.ru/public/widgets/feedback-widget?courseid={}&version={}'.format(get_course_scos_id(course_id),version)
    if api is None: 
        api = get_api_requester()
    resp = api.get(url,  headers=JSON_HEADER, timeout=1)
    if resp.status_code == 200:
        resp_data=(resp.text.encode('utf8'))
    return resp_data

def get_widget_url(course_id):
    try:
        data = get_course_scos_data(course_id)
        version = data['package']['items'][0]['business_version']    
        url = 'https://test.online.edu.ru/public/widgets/feedback-widget?courseid={}&version={}'.format(get_course_scos_id(course_id),version)
    except:
        url = ''
    return url

# def get_generic_id(course_id):
#     generic_id = ""
#     #filestore = '/edx/var/scos/courses/testplt/list.csv'
#     filestore = ENV('COURSES_DIR') + '/' + SCOS_COURSES_FILE
#     with open(filestore) as csv_file:
#         readCSV = csv.reader(csv_file, delimiter=';')
#         for row in readCSV:
#             if row[0] == str(course_id):
#                 generic_id = row[2]
#     return (generic_id)


def get_course_scos_id(course_key_string):
    # """Get SCOS course's identifier if exists"""
    try:
        course_key = CourseKey.from_string(course_key_string)
        course_module = modulestore().get_course(course_key)     
        if course_module.giturl:
            return course_module.giturl
        else:
            return None
    except:
        return None
    
  
def get_course_scos_data(course_key_string):
    course_key = CourseKey.from_string(course_key_string)                         
    course_module = modulestore().get_course(course_key)
    title = course_module.display_name
    details = CourseDetails.fetch(course_key)
    jsondetails = json.dumps(details, cls=CourseSettingsEncoder)
    jsondetails = json.loads(jsondetails)    
    
    if has_any_active_web_certificate(course_module):
        cert = "true"
    else:
        cert = "false"    

    content = jsondetails['overview']    
    duration = course_module.duration
    if not duration:
        duration = (datetime.datetime.strptime(jsondetails['end_date'], '%Y-%m-%dT%H:%M:%SZ')-datetime.datetime.strptime(jsondetails['start_date'], '%Y-%m-%dT%H:%M:%SZ')).days//7
    
    assessment_description = course_module.assessment_description
    accreditated = course_module.accreditated

    source_students = User.objects.filter(courseenrollment__course_id=course_key)
    visitors = course_module.max_student_enrollments_allowed or len(source_students) 

    if course_module.hours:
        hours = int(course_module.hours)
        
    if not course_module.hours_per_week:
        hours_per_week = 7
    else:
        hours_per_week = int(course_module.hours_per_week)
        
    teachers_json = jsondetails['instructor_info']
    for entry in teachers_json['instructors']:
        entry['display_name']= entry['name']
        entry['description']= entry['title']
        entry['image']= settings.LMS_ROOT_URL +entry['image']
          
    requirements = [course_module.requirements]
    competences = course_module.competences
 
    jsonfile = {
                "institution": "77e20215900e4ed1b5a424099fa19ff5",
                "title": title,
                "started_at": jsondetails['start_date'],
                "enrollment_finished_at": jsondetails['enrollment_end'],
                "finished_at": jsondetails['end_date'],                
                "image": settings.LMS_ROOT_URL + str(jsondetails['course_image_asset_path']),
                "description": jsondetails['short_description'],
                "competences":competences,
                "requirements": requirements,
                "content": content,
                "external_url": settings.LMS_ROOT_URL +"/courses/"+str(course_key_string)+"/about",
                "direction": jsondetails['learning_info'],  
                "duration": {"code": "week", "value": duration},  
                "lectures": len(course_module.discussion_topics), 
                "language": jsondetails['language'],
                "cert": cert, 
                "visitors": visitors,
                'teachers': jsondetails['instructor_info']['instructors'],  
                "transfers": [{'institution_id':'3928301200ea45e899d2e3a78a6db466',"direction_id" :jsondetails['learning_info'][0]}],
                "results": jsondetails['subtitle'],
                "accreditated": accreditated,
                "hours": hours,
                "hours_per_week": hours_per_week,
                "promo_url": "https://youtu.be/"+str(jsondetails['intro_video']),
                "promo_lang":  jsondetails['language'],
                "subtitles_lang": jsondetails['language'],

                "sessionid": course_key_string,
                "credits":float(jsondetails['effort']),
                "assessment_description": assessment_description
                                             }
    if course_module.enable_proctored_exams:
        jsonfile["proctoring_type"]= course_module.proctoring_type
        jsonfile["estimation_tools"]= course_module.estimation_tools
        jsonfile["proctoring_service"]= course_module.proctoring_service
                            
    if get_course_scos_id(course_key_string):
        jsonfile["id"]= get_course_scos_id(course_key_string)
    
    if course_module.business_version:
        jsonfile["business_version"] = int(course_module.business_version)
    else:
        jsonfile["business_version"] = 1
          
    data = {"partnerId": "3928301200ea45e899d2e3a78a6db466","package": {"items":[jsonfile]}}                             
    return data