# CoinPurse

Evan Young 2020  
cantis@gmail.com

## Overview
Coin Purse is supposed to be a *virtual wallet* for my Pathfinder character recording what they spend and what they spend it on and what the current balance of their account it. 

This is intended as a test bench for Python Flask programming, it has an sqlite database, migrations and a configuration file.

I'll document milestones here as I do them and my goals. 

Evan

## 10 Nov 2020
Should now add testing I think.

## 19 Nov
Got Pytest working... Note, I had to put a fix into ``` __init__ ``` that shouldn't be necessary

Also got code coverage working! execute the following

*Note: I have a .coveragerc file that limits the coverage data to the project source.*

** Generage the coverage data **  
``` PS> coverage run --source=. -m pytest```

** Show the report (command line) **  
``` PS> coverage report ```

** Generate the HTML Coverage report into **  
``` PS> coverage html ```

## 7 December
Got the entry code and tests to work and now I'm trying to deploy it to Google Cloud Run!\

## 13 December
Well the Google Cloud didn't work first time but I'll keep working on it
In the mean time I did add the code that produces a balance
I've added some enhancements and a bug to the issue tracker on github

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








