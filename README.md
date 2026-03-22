# Django-devtrack
Django app to create, view, read, issues / bugs inside a application. Back-end app to simply understand the django request and response flow.

## Features
- Create issues/bugs within an application
- View and read existing issues
- Back-end focused on Django request and response flow
- Simple understanding of Django fundamentals




## Images
![Issue Crated Diagram](./images/issue_created_img.png)




# Commands

- create django project named 'devtrack'
    ```bash 
    django-admin startproject devtrack .
    ```
- create app inside devtrack named 'issues' (command executed inside project i.e where manage.py is located)
    ```bash
    python manage.py startapp issues
    ```

    or 

    ```bash
    django-admin startapp issues
    ```

- run project
    ```bash
    python manage.py runserver
    ```

- allow scripts to run on powershell for current session only.
    ```bash
    Set-ExecutionPolicy Bypass -Scope Process
    ```
