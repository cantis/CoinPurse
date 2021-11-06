# Coin Purse DB notes

## Initialize DB object
To create the database at the command line execute:
*Note: this is different from the Migration based process below!
```powershell
# Create the database
PS python
>>>from web import db
>>>db.create_all()
>>>quit()
```
*Note: This works if working from nothing, if you have an existing database use the mirgration proces.*

## .pth file
See https://medium.com/@arnaud.bertrand/modifying-python-s-search-path-with-pth-files-2a41a4143574
For information on adding a .pth path file to the virtual environment site-packages file that contains the path to the application root from the terminal ($)
This seems to be important for testing and **migrations**.

## Migrations
N.B. this is dependant on flask_migrations being in the app and
initalized. Without this you won't get the right commands for the
following to work.

```powershell
# Iniatize migrations:
PS flask db init

# Add a new migration:
PS flask db migrate -m "migration name"

# Execute migration update:
PS flask db upgrade
```
## Note:
!! If we create the datbase using the create_all then the migration process won't recognise the changes, the db has to be 'behind' the current state.*

## To delete all tables on a Postgres database
*N.B. this leaves the database in place but with no tables.*

```powershell
# Open psql to edit the database
PS psql -U postgres
PS <enter password>
```

```postgresql
-- In psql prompt:
\l --list databases
\c  <database name> -- connect to the database
\dt --list the tables

drop schema <schema name> cascade; --drop the schema
create schema <schema name>; --create a new schema
grant all on <schema name> to postgres; --grant all privileges to postgres
grant all on <schema name> to public; --grant all privileges to public
\q --quit
```

