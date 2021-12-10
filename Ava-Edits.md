# Edits In Detailed
[-] Splitted The SETTINGS.py file into "Dev-Prod" in Settings DIR
    [-] "Dev-Prod" Extends from base.py
    === ===================================================================
    [-] edited manage.py file from:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-backend.settings')
    =
    TO: "For development.py Enviroment Settings"
    =
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-backend.settings.development') ==> *Change To ".Production" When Needed*
    === ===================================================================
    [-] Splitted INSTALLED_APPS Variable Into DJANGO_APPS/THIRD_PARTY_APPS/LOCAL_APPS for better app managment ==> *#Don't Duplicate Apps*
    === ===================================================================
    [-] Imported environ
        [-] Configured environ settings
        =
        env = environ.Env(DEBUG=(bool, False))
        environ.Env.read_env(env_file=".venv")
        =
        [-] Changed all enviromantal imports to env('#Variable Name')


[-] Moved All local apps to apps Dir
    [-] Edited each AppConfig *#"application dir" app.py file*
     Added "apps." ==> name = 'apps.#Application Dir Name#'
    -> *as "apps" stands for the main directory i moved the django-apps in*
    === ===================================================================
    [-] Edited LOCAL_APPS in settings to the new apps location inside apps dir
    === ===================================================================
    [-] Edited All The External App Imports inside all apps to apps.#appname.#etc


[-] Fixed all User Imports in all apps => Importing the User Model Directly
        => *Is A BAD Approach* 
    use:
    [=]
    from django.contrib.auth import get_user_model
    User = get_user_model()
    [=]
