import os
from os import environ

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
#
# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
# STATIC_URL = '/static/'
#
# # Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
# )


# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# don't share this with anybody.
SECRET_KEY = 'tkk^f^3otm#o*x@+#02@up5r9%zpls5jw-jfjp^_!ddvj-#_81'


DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'mlzzr'
# for security, best to set admin password in an environment variable
# ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')
ADMIN_PASSWORD = 'ycliangcf'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False


# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

# mturk_hit_settings = {
#     'keywords': ['easy', 'bonus', 'choice', 'study', 'economics'],
#     'title': 'Title for your experiment',
#     'description': 'Description for your experiment',
#     'frame_height': 500,
#     'minutes_allotted_per_assignment': 120,
#     'expiration_hours': 7*24, # 7 days
#     'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
#     'qualification_requirements': [
#         qualification.LocaleRequirement("EqualTo", "US"),
#         qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 95),
#         qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 1000),
#         qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
#     ]
# }


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [


# My own apps
    {
        'name': 'cf_iia',
        'display_name': "Belief Updating",
        'num_demo_participants': 9,
        'app_sequence': ['cf_update', 'cf_predict', 'cf_survey'],
        'participation_fee': 2.00,
        'mturk_hit_settings': {
            'keywords': ['easy', 'bonus', 'choice', 'study', 'economics'],
            'title': '40 Minutes STANFORD UNIVERSITY Economics Study - Earn BONUS of $1.5~$6',
            'description': 'We are conducting an academic survey on individual decision making. You will be asked a number of questions on how likely some events happen.',
            'frame_height': 800,
            'preview_template': 'global/MTurkPreview.html',
            'minutes_allotted_per_assignment': 120,
            'expiration_hours': 7*24, # 7 days
            'grant_qualification_id': '3SFGOZQ0QP9FTMWL37V9SYPG2VPC6V',# to prevent retakes
            'qualification_requirements': [
                qualification.LocaleRequirement("EqualTo", "US"),
                qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 97),
                qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 2000),
                qualification.Requirement('3SFGOZQ0QP9FTMWL37V9SYPG2VPC6V', 'DoesNotExist')
            ]
        },
    },
    {
        'name': 'cf_iia_strategy',
        'display_name': "Belief Updating (strategy)",
        'num_demo_participants': 9,
        'app_sequence': ['cf_strategy', 'cf_predict', 'cf_survey'],
        'participation_fee': 2.00,
        'mturk_hit_settings': {
            'keywords': ['easy', 'bonus', 'choice', 'study', 'economics'],
            'title': '40 Minutes STANFORD UNIVERSITY Economics Study - Earn BONUS of $1.5~$6',
            'description': 'We are conducting an academic survey on individual decision making. You will be asked a number of questions on how likely some events happen.',
            'frame_height': 800,
            'preview_template': 'global/MTurkPreview2.html',
            'minutes_allotted_per_assignment': 120,
            'expiration_hours': 7*24,  # 7 days
            'grant_qualification_id': '3SFGOZQ0QP9FTMWL37V9SYPG2VPC6V',# to prevent retakes
            'qualification_requirements': [
                qualification.LocaleRequirement("EqualTo", "US"),
                qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 97),
                qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 2000),
                qualification.Requirement('3SFGOZQ0QP9FTMWL37V9SYPG2VPC6V', 'DoesNotExist')
            ]
        },
    },
    {
        'name': 'EGB',
        'display_name': 'Discounting income flows',
        'num_demo_participants': 9,
        'app_sequence': ['EGB'],
        'participation_fee': 2.00,
        'mturk_hit_settings': {
            'keywords': ['easy', 'bonus', 'money', 'economics', 'study'],
            'title': '30 minutes STANFORD UNIVERSITY study: Earn up to $7.50',
            'description': 'We are conducting an academic survey on individual decision making. In the course of the study, we will ask you a number of questions about money. In addition to the HIT reward, you may receive up to $5.50 of bonus, depending on your answer.',
            'frame_height': 800,
            'preview_template': 'global/MTurkPreview3.html',
            'minutes_allotted_per_assignment': 120,
            'expiration_hours': 7*24,  # 7 days
            # 'grant_qualification_id': '36ME306TQB42ZI662XFAHMYGPTYSKD',# to prevent retakes
            'qualification_requirements': [
                qualification.LocaleRequirement("EqualTo", "US"),
                qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 97),
                # qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 2000),
                # qualification.Requirement('36ME306TQB42ZI662XFAHMYGPTYSKD', 'DoesNotExist')
            ]
        },
    },

]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
