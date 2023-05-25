# -*- coding: utf-8 -*-
"""SCOS courses management module"""

import sys
import os
import glob
import io
import simplejson as json
import csv
import exceptions
import fnmatch

from collections import OrderedDict

from openedx.features.scos.conf import ENV, SCOS_COURSES_FILE, COURSES_ID_PREFIX
from openedx.features.scos.lib import write_json
from openedx.features.scos.roo import get_course_scos_data
import shutil

scos_courses = None


def load_scos_courses_from_file(filename = None):
    global scos_courses
    if filename is None:
        filename = ENV('COURSES_DIR') + '/' + SCOS_COURSES_FILE
    scos_courses = {}
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter = ';')
        reader.fieldnames = 'id', 'title', 'scos_id'
        for row in reader:
            scos_courses[ row['id'].decode('utf-8') ] = {
            'title': row['title'].decode('utf-8'),
            'scos_id': row['scos_id'].decode('utf-8')
            }


def save_scos_courses_to_file(filename = None):
    """Save SCOS courses' data to file"""
    global scos_courses
    if filename is None:
        filename = ENV('COURSES_DIR') + '/' + SCOS_COURSES_FILE        
    if scos_courses is not None:
        with io.open(filename, mode = 'w+', encoding='utf-8') as f:
            for key, value in scos_courses.iteritems():
                f.write(unicode(key + ';'))
                f.write(unicode(value['title'] + ';'))
                f.write(unicode(value['scos_id'] + '\n'))
    else:
        raise exceptions.RuntimeError(
	        'scos_courses were not loaded yet')


def add_scos_course_to_list(course_id, title, scos_id):
    """Add SCOS course's data to file"""
    global scos_courses
    if scos_courses is None:
        load_scos_courses_from_file()
    scos_courses[course_id] = {
        'title': title,
        'scos_id': scos_id
    }
    save_scos_courses_to_file()


def remove_scos_course_from_list(course_id):
    """Remove SCOS course's data from file"""
    global scos_courses
    if scos_courses is None:
        load_scos_courses_from_file()
    del scos_courses[course_id]
    save_scos_courses_to_file()


def update_scos_course_in_list(course_id, title, scos_id):
    """Update SCOS course's data in file"""
    remove_scos_course_from_list(course_id)
    add_scos_course_to_list(course_id, title, scos_id)





# def create_course_from_default(course_id):
#     filename = course_id.replace(COURSES_ID_PREFIX, '')
#     shutil.copy(ENV('COURSES_DIR')+'/default.json', ENV('COURSES_DIR')+'/'+ filename + '.json')
#     return None




def upate_course_scos_data(course_id, dictionary):
    """Update SCOS course's data in file"""
    data = get_course_scos_data(course_id)
    if data is not None:
        for key, value in dictionary.iteritems():
            data['package']['items'][0][key] = value
            filename = course_id.replace(COURSES_ID_PREFIX, '')
            filename = ENV('COURSES_DIR') + '/' + filename + '.json'
            write_json(data, filename)
    else:
        raise exceptions.RuntimeError('SCOS metadata not found '
	        + 'for course ' + course_id)
 

def get_course_id_by_pattern(pattern):
    result = []
    for root, dirs, files in os.walk(ENV('COURSES_DIR')):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result[0]
