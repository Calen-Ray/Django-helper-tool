from django.core import management
import os
import re

# all file contents are stored seperately to maintain readable code. 
from djang_helper_supporting import project_url_contents, settings_file_contents


# for now these are hard-coded but the intention is to allow the user to chnage the name of any of these.
project_name = 'project_test'
custom_app = 'app_test'
user_app = 'users'
api_app = 'api'
time_zone = 'UTC'

print(f'starting project {project_name}')
management.call_command('startproject', project_name) # generate project 

print(f'starting app {custom_app}')
os.chdir(project_name) # change dir to project level to have access to manage.py
management.call_command('startapp', custom_app) # generate custom app

print(f'starting app {user_app} and {api_app}')
management.call_command('startapp', user_app) # generate users app
management.call_command('startapp', api_app) # generate api app


# lets change dir to the project level and add these apps to the urls.py and modify the settings.py
# to include our DRF as well as users app.
os.chdir(project_name)

print(f'modifying project url to include paths for {custom_app}, {user_app}, and {api_app}.')
with open('urls.py', 'w') as project_urls_file:
    project_urls_file.write(project_url_contents)

print(f'opening settings.py file for project.')
with open('settings.py', 'r') as projects_settings_file:
    saved_secret_key = re.findall( 'SECRET_KEY = .*', projects_settings_file.read())[0]
    print(f'found {saved_secret_key}')

print(f'modifying settings.py project file to include new apps and DRF settings as well as replacing the secret key.')
with open('settings.py', 'w') as projects_settings_file:
    projects_settings_file.write(re.sub('SECRET_KEY = .*',saved_secret_key,settings_file_contents.format(custom_app,api_app,user_app,time_zone)))
    print(f'injected oriignal {saved_secret_key}')



