# Some DB notes

## Initialize DB object
To create the database at the command line execute:
```
   $ python
   >>>from app import db
   >>>db.create_all()
   >>>quit()
```
## .pth file 
see https://medium.com/@arnaud.bertrand/modifying-python-s-search-path-with-pth-files-2a41a4143574
For information on adding a .pth path file to the virtual environment site-packages file that contains the path to the application root from the terminal ($)
This seems to be important for testing and **migrations**. 

## Migrations
N.B. this is dependant on flask_migrations being in the app and
initalized. Without this you won't get the right commands for the
following to work. 

Iniatize migrations: `$ flask db init`  
Add a new migration: `$ flask db migrate -m "migration name"`  
Execute migration update: `$ flask db upgrade`  
