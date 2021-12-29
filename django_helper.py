from django.core import management
import os
import re

# all file contents are stored seperately to maintain readable code. 
from djang_helper_supporting import project_url_contents, settings_file_contents
from djang_helper_supporting import css_content, vue_content, html_index_content, html_base_content
from djang_helper_supporting import api_urls_content, api_serializer_content, api_views_content
from djang_helper_supporting import users_forms_content, users_models_content, users_views_content, users_urls_content


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
    projects_settings_file.write(re.sub('SECRET_KEY = .*',saved_secret_key,settings_file_contents.format(custom_app,api_app,user_app,project_name,project_name,time_zone)))
    print(f'injected oriignal {saved_secret_key}')




# With the project level work done, we can move onto the apps, starting with users.
os.chdir(f'../{user_app}')

print(f'modifying users app..')

print(f'modifying users models.py..')
with open('models.py', 'w') as users_models_file:
    users_models_file.write(users_models_content)

print(f'modifying users views.py..')
with open('views.py', 'w') as users_views_file:
    users_views_file.write(users_views_content)

print(f'modifying users forms.py..')
with open('forms.py', 'w') as users_forms_file:
    users_forms_file.write(users_forms_content)

print(f'modifying users urls.py..')
with open('urls.py', 'w') as users_urls_file:
    users_urls_file.write(users_urls_content)


# Next app will be the api.
os.chdir(f'../{api_app}')

print(f'modifying api app..')

print(f'modifying api views.py..')
with open('views.py', 'w') as api_views_file:
    api_views_file.write(api_views_content)

print(f'modifying api serializers.py..')
with open('serializers.py', 'w') as api_serializer_file:
    api_serializer_file.write(api_serializer_content.format(user_app))

print(f'modifying api urls.py..')
with open('urls.py', 'w') as api_urls_file:
    api_urls_file.write(api_urls_content)



# lets build the template and static dirs now.. 
os.chdir('..')
os.mkdir('templates')
os.mkdir('static')

with open('templates/base.html', 'w') as html_file:
    html_file.write(html_base_content)

with open('templates/home.html', 'w') as html_file:
    html_file.write(html_index_content)

with open('static/app.js', 'w') as vue_file:
    vue_file.write(vue_content)

with open('static/style.css', 'w') as css_file:
    css_file.write(css_content)

# management.call_command('makemigrations', user_app)
# management.call_command('migrate', user_app)
management.call_command('makemigrations')
management.call_command('migrate')
