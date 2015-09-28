

Set up postgres for the application: ::
  CREATE ROLE nportalreg with PASSWORD 'change_me_now';
  CREATE DATABASE nportalreg WITH OWNER=nportalreg  ENCODING 'UTf8';
  grant all privileges on DATABASE nportalreg to nportalreg;
  ALTER ROLE nportalreg LOGIN;

install a virtualenv
--------------------
virtualenv venv-nportal

Source the virtualenv::

  source venv-nportal/bin/activate


Install the app
----------------
get the nportal app source::

  git clone   git@github.com:itd/nportal.git

install the requirements::

  pip install -r requirements

Note: To get the latest deform with Bootstrap3 goodness, I did this::

  pip install -e git+https://github.com/Pylons/deform.git#egg=deform

Prep the build::
  python setup.py develop


set up base mojo::
  initialize_nportal_db development.ini
