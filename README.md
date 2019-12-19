# Tattletrail check for Cabot

## Usage
Allows Cabot users to create a status check for a background process. Similar to a DeadmanSnitch, the service acts to ensure that processes stay running. It uses Tattletrail a server where background processes can 'check-in'.  Tattletrail is a simple REST wrapper over a REDIS server that allows users to monitor cron jobs/background processes that fail to check in within a specific interval.      If you do not wish to use Tattletrail, background jobs could talk directly to REDIS to tell Cabot they have 'checked-in'. 
 

## How to install:
You will need a REDIS server hosted somewhere in your environment.

### Use this file
[cabot-check-tattletrail](https://test.pypi.org/project/cabot-check-tattletrail/)

##### As example: 

```RUN pip install -i https://test.pypi.org/simple/ cabot-check-tattletrail==0.9.0```

## How to deploy:

[Deployment process](https://github.com/objectstoragesolutions/cabot-check-tattletrail/wiki/How-to-deploy.)

## Learn more about TattleTrail

TattleTrail the server acts as a wrapper around REDIS and allows processes to 'check-in' while they are alive at regular intervals. 

[TattleTrail](https://github.com/objectstoragesolutions/tattletrail)

## Sponsors

We want to thank Excell Solutions for funding this open source project.

[Excell Solutions](http://www.excell.solutions/)

