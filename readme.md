# CoinPurse

Evan Young 2020
cantis@gmail.com

This file is my notes on my progress, keeping a record of what I've done and what I'm working on.

## Overview
Coin Purse is a *virtual wallet* for Pathfinder characters. Recording what they spend and what they spend it on and what the current balance their purse is.

This is intended as a test bench for Python Flask programming, it has an sqlite database, migrations, configuration file and docker support.

I'll document milestones here as I do them, my goals and plans.

Evan

## 12 Oct 2020
Initial Commit to Github

## 10 Nov
Adding testing setup

## 19 Nov
Got Pytest working... Note, I had to put a fix into ``` __init__ ``` that shouldn't be necessary

Also got code coverage working! execute the following

*Note: I have a .coverage file that limits the coverage data to the project source.*

```powershell
# Generate the coverage data **
PS coverage run --source=. -m pytest

# Show the report (command line) **
PS coverage report

# Generate the HTML Coverage report into **
PS coverage html
```


## 7 December
Got the entry code and tests to work and now I'm trying to deploy it to Google Cloud Run!

## 13 December
Well the Google Cloud didn't work first time but I'll keep working on it. In the mean time I did add the code that produces a balance. I've added some enhancements and a bug to the issue tracker on github.

## 30 December
I've spent some time re-looking at docker and I'm re-setting docker and adding a docker-compose.
Still having issues getting this running locally, so I can uderstand if it doesn't work when published.
I can get this running I have a series of updates to add:
- Customize add entry form
- Split functionality into blueprints
- add user login
- add login admin

## 31 December
Well, finally got the Docker / Docker-Compose to work i.e. run and be able to be hit! So, now on to some other work
the entry form.
Acomplished Today:
- Customized Add Entry

## 8 January 2021
Finished a major re-orgainzation of the app just before work today. Moved the Entry and Customer code into their own modules I think that's the right Python term) and I'm now using blueprints. Added a `wsgi.py` file to start it off and just generally suffled around everything.

This triggered fixes to the tests and their fixtures that took a coupld of days to sort out.

As silly as it sounds the character and entry folders are just this plain grey in my material icons set and I'd like them to be something else, but I have no idea how to do that and I'm resisting thinking on it too hard.

The application is now built in a factory class in the app `__init__.py`. This allows the factory to be called from the `wsgi.py` or from the pytest fixtures and the factory is really simple and clean.

I am noticing that even a simple flask web application now has A LOT of files to it.

Somewhere along the line I've also broken the visual studio docker run config, want to fix that.

## 14 January Google Auth not...
Giving up on the google auth at the moment, it turns out that it's a fair committment. So next up...
- Session 'memory' load last used session
- Session filter so we see only one session at a time
- Output to csv of records
- Load csv data back in?

## 17 January
Got the settings system split out to save the session to disk and I was able to get it to load the last used session

## 28 January
Added a Game Session filter, so you can look at the Entries for that session only. This also required a cleanup of the settings storage. I moved the 'session' code out of the routes and other modules and it's only used in the utility. Essentially I use the session object as a cache if a value is in the session I return that vs. hitting the Database if it isn't I retrieve it. This has required a re-work of the testing to make sure we are inside an application context that provides a session object
to flask so this works, this has been done as well.

## 5 February
Some significant progress, did a re-factor and moved to a functional application structure model. Moved the `wsgi.py` file to the root of the project and re-factored the links. That got the docker setup working. Fixed the database creation code so the dabase now builds a new datbase properly, see the db_notes for instructions on how to create the datbase. Next up is reporting using the google sheets API.

## 9 February
Well, after a fight, got the Flask_Login working. You'll want to pay attenton to where the parts of this are actually configured. The examples showed the LoginManager - UserLoader being configured in the application factory `__init__.py`. In this case I set up the auth blueprint in the factory but the rest is done in the User Model. I was gettign all kinds of metadata errors and ALL of the tests jammed. The re-configuration as I have it now works.

## 18 March
Finally got my docker bind mount working! The VSCode Docker extension is really good for providing the ability to drill in to a running container and see it's structure. Once I could see into the container I was able to adjust where the folder was being created.

Interestingly, no docker volume is actually created for the bind mount it just creates what looks like a normal folder and the app running in the container can see it. Oh, importantly, I have to block the folder from being created as part of the image in the .dockerignore

## 27 August
Been a while but I've been updating this app again and I was able to publish it up to Heroku, yea it's not a very big deal but it's nice to have a cloud deployment up! I did find out that the settings system is just 'wrong' I didn't account for multiple users so I have to do a re-write of the settings system. This also involves re-learning how to use the flask-migrate package as I now need to make db changes on the Heroku System.

## 13 September
Finally got my setttings tests working better, the settings system is still a mess but at least I can now properly test it.

## 31 October
Something wrong on the DB level, it appears to be in the production Postgres database. I've re-done the migrations but it still seems wrong.

## 6 November
Changed some documenatation and I'm fixiup that postgres error. Turns out that the postgres error was a query problem. If you have a Distinct and an Order by in the same query on postgres you get an error where the DB can't figure out how to sort and be distinct at the same time IF you don't have the column you're soritng by in the distinct. I cleared that and it appears to be working now. See https://stackoverflow.com/questions/12693089/pgerror-select-distinct-order-by-expressions-must-appear-in-select-list

I also fixed up some documentation today, re-deployed to Heroku and got it updated again and I'm cleaning up some of the game session code. Set the master branch to only allow PR commits directly. All of the tests are passing. After the clean up I'm going to set this asside for a bit and switch to another project.
