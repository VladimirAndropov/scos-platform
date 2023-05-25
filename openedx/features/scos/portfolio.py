# -*- coding: utf-8 -*-
import requests
import json
import datetime
import pytz
import exceptions

from openedx.features.scos.conf import ENV, HTTP_TIMEOUT, TESTING, DEBUG_OUTPUT_FILE \
    ,SSL_CERT, SSL_KEY, VERBOSE, console
from openedx.features.scos.lib import ServerSession, ImpatientHTTPAdapter \
    ,JSON_HEADER, write_json, logit
from openedx.features.scos.roo import get_course_scos_id, get_course_scos_data, get_api_requester
from openedx.features.scos.users import get_user_scos_id, get_user_scos_ids

api = None


# def get_api_requester():
#     session = requests.Session()
#     #url = ENV('API_URL')+"v1/connection/check"
#     url = "https://test.online.edu.ru/api/v1/connection/check"
#     #session.get(url,  headers=JSON_HEADER, cert=(SSL_CERT, SSL_KEY))   
#     session.get(url,  headers=JSON_HEADER, cert=(SSL_CERT, SSL_KEY))
#     return session

def enroll_scos_user(cid, uid):
    # """Enroll user to course in portfolio"""
    global api
    scos_cid = get_course_scos_id(cid)
    if scos_cid is None:
        return False
    scos_uid = get_user_scos_id(uid)
    if scos_uid is None:
        return False
    
    now = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S%z')
    # add_enrollment(scos_cid, scos_uid, now_str)
    scos_data = get_course_scos_data(cid)
    post_data = {
        'courseId': scos_cid,
        'sessionId': cid,
        'usiaId': scos_uid,
        'enrollDate': now_str,
        'sessionStart': scos_data['package']['items'][0]['started_at'],
        'sessionEnd': scos_data['package']['items'][0]['finished_at']
        }
    if api is None:
        api = get_api_requester()
    url = 'v1/course/enroll'
    resp = api.post(url, data = json.dumps(post_data) ,headers = JSON_HEADER)
    if resp.status_code == 201:
        return True
    else:
        return False


def unenroll_scos_user(cid, uid):
    global api
    scos_cid = get_course_scos_id(cid)
    if scos_cid is None:
        return False
    scos_uid = get_user_scos_id(uid)
    if scos_uid is None:
        return False
    post_data = {
        'courseId': scos_cid,
        'sessionId': cid,
        'usiaId': scos_uid
        }

    if api is None:
        api = get_api_requester()

    url = 'v1/course/unenroll'
    resp = api.post(url ,data = json.dumps(post_data) ,headers = JSON_HEADER)
    return resp



def check_scos_enrollment(cid, uid):
    # """Check if user is enrolled in course in portfolio"""
    global api
    scos_cid = get_course_scos_id(cid)
    if scos_cid is None:
        return False
    scos_uid = get_user_scos_id(uid)
    if scos_uid is None:
        return False
    
    url = 'v1/course/checkenroll'
    post_data = {
        'courseId': scos_cid,
        'sessionId': cid,
        'usiaId': scos_uid
    }
        
    if api is None:
        api = get_api_requester()
        
    resp = api.post(
        url, data=json.dumps(post_data), headers=JSON_HEADER
    )
    
    resp_data = resp.json()
    return resp_data['data']



def post_result(cid, uid, timestamp, rating, progress, checkpointName, checkpointId):
    # """Send user's atomic result to porfolio"""
    global api
    scos_cid = get_course_scos_id(cid)
    if scos_cid is None:
        return False
    scos_uid = get_user_scos_id(uid)
    if scos_uid is None:
        return False
    # if check_scos_enrollment(cid, uid) == u'PARTICIPATION_NOT_FOUND':
    #     enroll_scos_user(cid, uid)
    tz = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(tz)
    now_str = now.strftime('%Y-%m-%dT%H:%M:%S%z')
    post_data = {
        'courseId': scos_cid,
        'sessionId': cid,
        'usiaId': scos_uid,
        'date': now_str,
        'rating': rating,
        'progress': progress,
        # 'proctored': 'examus',
        'checkpointName': checkpointName,
        'checkpointId': checkpointId
        }
    
    if api is None:
        api = get_api_requester()
        
    url = 'v1/course/results/add'
    resp = api.post(
        url
        ,data = json.dumps(post_data)
        ,headers = JSON_HEADER
        )
    
    logit('Result posted'
          + '  scos_cid: ' + scos_cid + '  scos_uid: ' + scos_uid
          + '  status: ' + str(resp.status_code)
          + '  response: ' + resp.text)
    
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        return False
    
    return True


def post_result_mark(cid, uid, mark):
    # """Send user's atomic result to porfolio"""
    global api
    scos_cid = get_course_scos_id(cid)
    scos_uid = get_user_scos_id(uid)  

    # scos_uid = 'fae8ffc0-c039-4526-a717-96f0f7cea172'
    # scos_cid = '1846d1bd-1f3c-4269-9e18-a61dbdc715cd'
    # cid = 'course-v1:fa+digitalmarket+2019_leto'
    # mark = '3'

    if scos_cid is None:
        return False

    if scos_uid is None:
        return False
    # if not enrollment_exists(scos_cid, scos_uid):
    #     return False
    
    post_data = [{
        'course_id': scos_cid,
        'session_id': cid,
        'user_id': scos_uid,
        'mark': mark
        }]
    
    if api is None:
        api = get_api_requester()
        
    url = 'v2/courses/participation/mark'
    resp = api.post(
        url
        ,data = json.dumps(post_data)
        ,headers = JSON_HEADER
        )
    
    
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError:
        return False
    
    return True


def post_cert(username, cid):
    return


def get_mark_batch(user_ids, cid):
    # user_ids = ["930", "35"]
    # scos_uid1 = 'fae8ffc0-c039-4526-a717-96f0f7cea172'
    # scos_uid2 = 'fbd0c270-bc21-46d6-b11b-3d5dea7734b4'
    # scos_uids = [scos_uid1, scos_uid2]
    # scos_cid = '1846d1bd-1f3c-4269-9e18-a61dbdc715cd'
    # cid = 'course-v1:fa+digitalmarket+2019_leto'
    global api
    scos_cid = get_course_scos_id(cid)
    scos_uids = get_user_scos_ids(user_ids)
    post_data = {
        'course_id': scos_cid,
        'session_id': cid,
        'user_ids': scos_uids
        }
    if api is None:
        api = get_api_requester()
    url = 'v2/courses/participation/mark/list'
    resp = api.post(
        url, data=json.dumps(post_data), headers=JSON_HEADER
        )
    return resp

def post_mark_batch(user_ids, cid):
    # user_ids = ["930", "35"]
    # scos_uid1 = 'fae8ffc0-c039-4526-a717-96f0f7cea172'
    # scos_uid2 = 'fbd0c270-bc21-46d6-b11b-3d5dea7734b4'
    # scos_uids = [scos_uid1, scos_uid2]
    # scos_cid = '1846d1bd-1f3c-4269-9e18-a61dbdc715cd'
    # cid = 'course-v1:fa+digitalmarket+2019_leto'
    global api
    scos_cid = get_course_scos_id(cid)
    scos_uids = get_user_scos_ids(user_ids)

    post_data = {"list":[
        {
        "courseId": scos_cid,
        "sessionId": cid,
        "usiaId": scos_uid1,
        "progress": 35
        },
    ]}
    if api is None:
        api = get_api_requester()
    url = 'v1/course/results/progress/add/batch'
    resp = api.post(url, data=json.dumps(post_data), headers=JSON_HEADER)
    return resp
