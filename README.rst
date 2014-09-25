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


