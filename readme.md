# CoinPurse

Evan Young 2020  
cantis@gmail.com

## Overview
Coin Purse is supposed to be a *virtual wallet* for my Pathfinder character recording what they spend and what they spend it on and what the current balance of their account it. 

This is intended as a test bench for Python Flask programming, it has an sqlite database, migrations and a configuration file.

I'll document milestones here as I do them and my goals. 

Evan

## 10 Nov
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
Got the entry code and tests to work and now I'm trying to deploy it to Google Cloud Run!



