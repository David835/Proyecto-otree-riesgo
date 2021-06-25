import os
from os import environ
import dj_database_url
import otree.settings


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 3.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'single_fixed',
        'display_name': "RiskOther - SINGLE Fixed",
        'num_demo_participants': 2,
        'participation_fee': 4.00,
        'app_sequence': ['single'],
        'compensation': 'fixed',     # Enter either fixed, variable_result or variable_profit
    },
    {
        'name': 'single_result',
        'display_name': "RiskOther - SINGLE Variable Result",
        'num_demo_participants': 2,
        'participation_fee': 4.00,
        'app_sequence': ['single'],
        'compensation': 'variable_result',     # Enter either fixed, variable_result or variable_profit
    },
    {
        'name': 'single_profit',
        'display_name': "RiskOther - SINGLE Variable Profit",
        'num_demo_participants': 2,
        'participation_fee': 4.00,
        'app_sequence': ['single'],
        'compensation': 'variable_profit',     # Enter either fixed, variable_result or variable_profit
    },
    {
        'name': 'group_fixed',
        'display_name': "RiskOther - GROUP Treatment Fix",
        'num_demo_participants': 6,
        'participation_fee': 4.00,
        'app_sequence': ['group'],
        'compensation': 'fixed',     # Enter either fixed, variable_result or variable_profit

    },
    {
        'name': 'group_result',
        'display_name': "RiskOther - GROUP Treatment Variable Result",
        'num_demo_participants': 6,
        'participation_fee': 4.00,
        'app_sequence': ['group'],
        'compensation': 'variable_result',     # Enter either fixed, variable_result or variable_profit

    },
    {
        'name': 'group_profit',
        'display_name': "RiskOther - GROUP Treatment Variable Profit",
        'num_demo_participants': 6,
        'participation_fee': 4.00,
        'app_sequence': ['group'],
        'compensation': 'variable_profit',     # Enter either fixed, variable_result or variable_profit

    },
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [   
    {
        'name': 'awi_lab',
        'display_name': 'AWI Experimentallabor',
        'participant_label_file': 'participant_labels.txt'
    }
]


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

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '85a3wt+4h@pyalkamnuk2@22(qm75%uf81=(jddp%doud=oxyp'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#DATABASES = {
   # 'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
       # default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
   # )
#}


# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


otree.settings.augment_settings(globals())
