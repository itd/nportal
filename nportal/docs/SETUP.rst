

Set up postgres for the application: ::
  CREATE ROLE nportalreg with PASSWORD 'change_me_now';
  CREATE DATABASE nportalreg WITH OWNER=nportalreg  ENCODING 'UTf8';
  grant all privileges on DATABASE nportalreg to nportalreg;
  ALTER ROLE nportalreg LOGIN;

set up base mojo::
  initialize_nportal_db development.ini
