# -*- coding: utf-8 -*-
"""Package configuration module"""

import os
from django.conf import settings

TESTING = False
VERBOSE = True

DATA_DIR = '/edx/var/scos'
LOG_FILE = DATA_DIR + '/log.txt'
DEBUG_OUTPUT_FILE = DATA_DIR + '/debug.json'

SCOS_USERS_FILE = DATA_DIR + '/users.json'
KEEP_SCOS_USERS_IN_MEM = True
SCOS_ENROLLMENTS_FILE = DATA_DIR + '/enrollments.csv'
KEEP_SCOS_ENROLLMENTS_IN_MEM = True

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
SSL_CERT = MODULE_DIR + '/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.crt'
SSL_KEY = MODULE_DIR + '/keys/bc007e88-0e4b-4a1a-975a-8aecca36542d.key'

SCOS_COURSES_FILE = 'list.csv'
COURSES_ID_PREFIX = 'course-v1:'
WIDGET_TEMPLATE_FILE = 'widget_template.html'

HTTP_TIMEOUT = 5

RU_STR = {
'Course reviews': 'Reviews'
}

DEFAULT_ENV = 'PROD'

ENVS = {}
ENVS['PROD'] = {
	'NAME': 'PROD',
	'PLATFORM_ID': settings.PLATFORM_ID,
	'INSTITUTION_ID': settings.INSTITUTION_ID,
	'DOMAIN': settings.DOMAIN,
	'API_URL': settings.API_URL,
	'API_USER': settings.API_USER,
	'API_USER_ID': settings.API_USER_ID,
	'API_PASSWORD': settings.API_PASSWORD,
	'PORTFOLIO_API_URL': settings.PORTFOLIO_API_URL,
	'COURSES_DIR': DATA_DIR + '/courses/prod'
}


current_env = ENVS[DEFAULT_ENV]

console = False


def set_environment(name):
	global current_env
	current_env = ENVS[name]


def ENV(var, env_name = None):
	if env_name is None:
		return current_env[var]
	else:
		return ENVS[env_name][var]
