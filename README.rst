===================
Askbot - Q&A forum
===================

This is Askbot project - open source Q&A system, like StackOverflow, Yahoo Answers and some others.
Askbot is based on code of CNPROG, originally created by Mike Chen 
and Sailing Cai and some code written for OSQA.

Demos and hosting are available at http://askbot.com.

How to contribute
=================

**Translators: DO NOT use git to contribute translations!!!** instead - translate at https://www.transifex.com/projects/p/askbot/.

All documentation is in the directory askbot/doc

To contribute code, please fork and make pull requests.

If you are planning to add a new feature, please bring it up for discussion at our forum
(http://askbot.org/en/questions/) and mention that you are willing to develop this feature.

We will merge obvious bug fixes without questions, for more complex fixes
please add a test case that fails before and passes after applying your fix.

**Notes on using git for Askbot.** Please use topic branches only - one per feature or bugfix.
Do not add multiple features and fixes into the same branch -
those are much harder to understand and merge.

Follow https://help.github.com/articles/fork-a-repo to to learn how to use
`fetch` and `push` as well as other help on using git.

License, copyright and trademarks
=================================
Askbot software is licensed under GPL, version 3.

Copyright Askbot S.p.A and the project contributors, 2010-2013.

"Askbot" is a trademark and service mark registered in the United States, number 4323777.



Askbot as App in existing project 
=========================================

1. install askbot
git clone repo
cd to apps directory in Mac
git clone git://github.com/vinodpandey/askbot-devel.git

vagrant ssh
cd /vagrant 
source bin/activate
cd code/apps/askbot-devel
sudo /vagrant/bin/python setup.py install
sudo /vagrant/bin/pip uninstall django-followit
sudo /vagrant/bin/pip install -e git://github.com/vinodpandey/django-followit@v1.0#egg=followit

update settings/base.py with askbot config and django-allauth askbot specific configuration
update settings/dev.py with askbot specific configuration
update DATABASES in settings/base.py to add MySQL specific 2 entries
update urls.py to add askbot specific URLs

add TEMPATE_LOADERS as [] - if it is already not there in settings/base.py
add PROJECT_ROOT to settings/base.py


>> askbot/models/user.py - near line 401 - class AuthUserGroups(models.Model): - db_table_name should be the name of custom_user table
python manage.py syncdb
python manage.py migrate
python manage.py collectstatic

check if django_custom_auth is updated or not. If not, them manually update the table using sql script to add missing columns.


====

-- --------------------------------------------------------

--
-- Table structure for table `django_custom_auth_user`
--
ALTER TABLE `django_custom_auth_user`
ADD COLUMN   `status` varchar(2) NOT NULL,
ADD COLUMN   `is_fake` tinyint(1) NOT NULL,
ADD COLUMN   `email_isvalid` tinyint(1) NOT NULL,
ADD COLUMN   `email_key` varchar(32) DEFAULT NULL,
ADD COLUMN   `reputation` int(10) unsigned NOT NULL,
ADD COLUMN   `gravatar` varchar(32) NOT NULL,
ADD COLUMN  `avatar_type` varchar(1) NOT NULL,
ADD COLUMN   `gold` smallint(6) NOT NULL,
ADD COLUMN   `silver` smallint(6) NOT NULL,
ADD COLUMN   `bronze` smallint(6) NOT NULL,
ADD COLUMN   `questions_per_page` smallint(6) NOT NULL,
ADD COLUMN   `last_seen` datetime NOT NULL,
ADD COLUMN   `real_name` varchar(100) NOT NULL,
ADD COLUMN   `website` varchar(200) NOT NULL,
ADD COLUMN  `location` varchar(100) NOT NULL,
ADD COLUMN   `country` varchar(2) NOT NULL,
ADD COLUMN   `show_country` tinyint(1) NOT NULL,
ADD COLUMN   `date_of_birth` date DEFAULT NULL,
ADD COLUMN   `about` longtext NOT NULL,
ADD COLUMN   `interesting_tags` longtext NOT NULL,
ADD COLUMN   `ignored_tags` longtext NOT NULL,
ADD COLUMN   `subscribed_tags` longtext NOT NULL,
ADD COLUMN   `email_signature` longtext NOT NULL,
ADD COLUMN   `show_marked_tags` tinyint(1) NOT NULL,
ADD COLUMN   `email_tag_filter_strategy` smallint(6) NOT NULL,
ADD COLUMN   `display_tag_filter_strategy` smallint(6) NOT NULL,
ADD COLUMN   `new_response_count` int(11) NOT NULL,
ADD COLUMN   `seen_response_count` int(11) NOT NULL,
ADD COLUMN   `consecutive_days_visit_count` int(11) NOT NULL,
ADD COLUMN   `languages` varchar(128) NOT NULL,
ADD COLUMN   `twitter_access_token` varchar(256) NOT NULL,
ADD COLUMN   `twitter_handle` varchar(32) NOT NULL,
ADD COLUMN   `social_sharing_mode` int(11) NOT NULL;

====



python manage.py add_missing_subscriptions
TransactionManagementError: Transaction managed block ended with pending COMMIT/ROLLBACK



=============
If you are adding Askbot to a django site that already has registered users, please see this section.

There are two caveats.

Firstly, if you are using some other login/registration app, please disable feature “settings”->”data entry and display”->”allow posting before logging in”.

This may be fixed in the future by adding a snippet of code to run right after the user logs in - please ask at askbot forum if you are interested.

Secondly, disable setting “settings”->”user settings”->”allow add and remove login methods”. This one is specific to the builtin login application which allows more than one login method per user account.
==============
If you already have a django site with users, after adding askbot to your project, run a management command just once:

python manage.py add_missing_subscriptions
==============



python manage.py runserver 


Errors:
can't subtract offset-naive and offset-aware datetimes
Solution: USE_TZ = False

KeyError at /settings/QA_SITE_SETTINGS/
Solution:
LANGUAGE_CODE = 'en'

Custom templates
ASKBOT_EXTRA_SKINS_DIR = os.path.join(PROJECT_ROOT, 'apps', 'askbot_templates')
askbot_templates
- websitename
- - templates


Note:  
1. while running in production mode, make sure memcached is up and running otherwise it will show errors regarding
live settings and language code
2. custom auth module name should be django_custom_auth only. This is hardcoded in https://github.com/vinodpandey/askbot-devel/blob/master/askbot/models/user.py
Line 386
class AuthUserGroups(models.Model):
      """explicit model for the auth_user_groups bridge table.
      """
      group = models.ForeignKey(AuthGroup)
      user = models.ForeignKey(User)
      class Meta:
      app_label = 'auth'
      unique_together = ('group', 'user')
      #change this to the custom user model
      #db_table = 'auth_user_groups'
      db_table = 'custom_auth_user_groups'
      managed = False




urls.py
=========

###### ASKBOT URLs ##############

urlpatterns += patterns('',  
                       (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))  
                        )  
 
urlpatterns += patterns('',  
                        (r'^followit/', include('followit.urls')),  
                        (r'^tinymce/', include('tinymce.urls')),  
                        (r'^robots.txt$', include('robots.urls')),  
                        )  





##################################  



settings.py
=============

USE_TZ = False  
LANGUAGE_CODE = 'en'  

############### using django-allauth with askbot #####################  

LOGIN_URL = '/accounts/login/'  
LOGOUT_URL = '/accounts/logout/'  
LOGOUT_REDIRECT_URL = "/"  

#####################################################################  

########### ASKBOT specific configuration #################################################################  
###########################################################################################################  
import askbot  
import site  
#this line is added so that we can import pre-packaged askbot dependencies  
ASKBOT_ROOT = os.path.abspath(os.path.dirname(askbot.__file__))  
site.addsitedir(os.path.join(ASKBOT_ROOT, 'deps'))  

TEMPLATE_LOADERS.insert(0, 'askbot.skins.loaders.Loader')  


MIDDLEWARE_CLASSES.append('askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware')  
MIDDLEWARE_CLASSES.append('askbot.middleware.forum_mode.ForumModeMiddleware')  
MIDDLEWARE_CLASSES.append('askbot.middleware.cancel.CancelActionMiddleware')  
MIDDLEWARE_CLASSES.append('django.middleware.transaction.TransactionMiddleware')  
MIDDLEWARE_CLASSES.append('askbot.middleware.view_log.ViewLogMiddleware')  
MIDDLEWARE_CLASSES.append('askbot.middleware.spaceless.SpacelessMiddleware')  


#UPLOAD SETTINGS  
FILE_UPLOAD_TEMP_DIR = os.path.join(  
                                os.path.dirname(__file__),  
                                'tmp'  
                            ).replace('\\','/')  

FILE_UPLOAD_HANDLERS = (  
    'django.core.files.uploadhandler.MemoryFileUploadHandler',  
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',  
)  
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')  
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes  
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'  

TEMPLATE_CONTEXT_PROCESSORS.insert(0,'askbot.context.application_settings')  
TEMPLATE_CONTEXT_PROCESSORS.insert(1,'askbot.user_messages.context_processors.user_messages')  

INSTALLED_APPS.append('compressor')  
INSTALLED_APPS.append('askbot')  
INSTALLED_APPS.append('askbot.deps.livesettings')  
INSTALLED_APPS.append('keyedcache')  
INSTALLED_APPS.append('robots')  
INSTALLED_APPS.append('django_countries')  
INSTALLED_APPS.append('djcelery')  
INSTALLED_APPS.append('djkombu')  
INSTALLED_APPS.append('followit')  
INSTALLED_APPS.append('tinymce')  
INSTALLED_APPS.append('group_messaging')  



#setup memached for production use!  
#see http://docs.djangoproject.com/en/1.1/topics/cache/ for details  
#CACHE_BACKEND = 'locmem://'  
#needed for django-keyedcache  
CACHE_TIMEOUT = 6000  
#sets a special timeout for livesettings if you want to make them different  
LIVESETTINGS_CACHE_TIMEOUT = CACHE_TIMEOUT  
#CACHE_PREFIX = 'askbot' #make this unique  
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True  
#If you use memcache you may want to uncomment the following line to enable memcached based sessions  
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'  


CACHES = {  
    'default': {  
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache'  ,
        'LOCATION': '127.0.0.1:11211',  
        'TIMEOUT': CACHE_TIMEOUT,  
        'OPTIONS': {  
            'MAX_ENTRIES': 1000  
        },  
        'KEY_PREFIX': 'askbot'  
    }  
}  


###########################  
#
#   this will allow running your forum with url like http://site.com/forum  
# 
#   ASKBOT_URL = 'forum/'  
#
ASKBOT_URL = '' #no leading slash, default = '' empty string  
ASKBOT_TRANSLATE_URL = True #translate specific URLs  
_ = lambda v:v #fake translation function for the login url  
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL,_('accounts/'),_('login/'))  
#LOGIN_REDIRECT_URL = ASKBOT_URL #adjust, if needed  
#note - it is important that upload dir url is NOT translated!!!  
#also, this url must not have the leading slash  
ALLOW_UNICODE_SLUGS = False  
ASKBOT_USE_STACKEXCHANGE_URLS = False #mimic url scheme of stackexchange  

#Celery Settings  
BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"  
CELERY_ALWAYS_EAGER = True  

import djcelery  
djcelery.setup_loader()  
DOMAIN_NAME = ''  

CSRF_COOKIE_NAME = '_csrf'  
#https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/  
#CSRF_COOKIE_DOMAIN = DOMAIN_NAME  

STATIC_ROOT = os.path.join(PROJECT_CODE_PATH, "static")  
STATICFILES_DIRS = (  
    ('default/media', os.path.join(ASKBOT_ROOT, 'media')),  
)  
STATICFILES_FINDERS = (  
    'django.contrib.staticfiles.finders.FileSystemFinder',  
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  
    'compressor.finders.CompressorFinder',  
)  

RECAPTCHA_USE_SSL = True  

#HAYSTACK_SETTINGS  
ENABLE_HAYSTACK_SEARCH = False  
#Uncomment for multilingual setup:  
#HAYSTACK_ROUTERS = ['askbot.search.haystack.routers.LanguageRouter',]  

#Uncomment if you use haystack  
#More info in http://django-haystack.readthedocs.org/en/latest/settings.html  
#HAYSTACK_CONNECTIONS = {  
#            'default': {
#                        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',  
#            }  
#}  


TINYMCE_COMPRESSOR = True  
TINYMCE_SPELLCHECKER = False  
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'default/media/js/tinymce/')  
#TINYMCE_JS_URL = STATIC_URL + 'default/media/js/tinymce/tiny_mce.js'  
TINYMCE_DEFAULT_CONFIG = {  
    'plugins': 'askbot_imageuploader,askbot_attachment',  
    'convert_urls': False,  
    'theme': 'advanced',  
    'content_css': STATIC_URL + 'default/media/style/tinymce/content.css',  
    'force_br_newlines': True,  
    'force_p_newlines': False,  
    'forced_root_block': '',  
    'mode' : 'textareas',  
    'oninit': "TinyMCE.onInitHook",  
    'plugins': 'askbot_imageuploader,askbot_attachment',  
    'theme_advanced_toolbar_location' : 'top',  
    'theme_advanced_toolbar_align': 'left',  
    'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',  
    'theme_advanced_buttons2': '',  
    'theme_advanced_buttons3' : '',  
    'theme_advanced_path': False,  
    'theme_advanced_resizing': True,  
    'theme_advanced_resize_horizontal': False,  
    'theme_advanced_statusbar_location': 'bottom',  
    'width': '730',  
    'height': '250'  
}

#delayed notifications, time in seconds, 15 mins by default  
NOTIFICATION_DELAY_TIME = 60 * 15  

GROUP_MESSAGING = {  
    'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',  
    'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}  
}  

ASKBOT_MULTILINGUAL = False  

ASKBOT_CSS_DEVEL = False  
if 'ASKBOT_CSS_DEVEL' in locals() and ASKBOT_CSS_DEVEL == True:  
    COMPRESS_PRECOMPILERS = (  
        ('text/less', 'lessc {infile} {outfile}'),  
    )  

COMPRESS_ENABLED = False  
COMPRESS_JS_FILTERS = []  
COMPRESS_PARSER = 'compressor.parser.HtmlParser'  
JINJA2_EXTENSIONS = ('compressor.contrib.jinja2ext.CompressorExtension',)  

# Use syncdb for tests instead of South migrations. Without this, some tests  
# fail spuriously in MySQL.  
SOUTH_TESTS_MIGRATE = False  

VERIFIER_EXPIRE_DAYS = 3  

ASKBOT_SELF_TEST = False  

ASKBOT_EXTRA_SKINS_DIR = os.path.join(PROJECT_CODE_PATH, 'apps', 'askbot_templates')  

########### ASKBOT specific configuration #################################################################  
###########################################################################################################  








