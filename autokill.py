#!/usr/bin/env python

###
# autokill for Saltstack.
#
# This script will run and kill off any hung up Salt jobs which may be lingering on your salt master server. The goal of this script is to keep the number of stuck processes from overloading
# your salt-master. I work in a "highly dynamic" environment which can cause issues with minions reporting back promptly. To keep things sane on my salt-master, I generally terminate any jobs
# taking over an hour to complete. It's been running on my 2018.3.0 (Oxygen) salt master for 1+ years without an issue.
#
# Want to see it work without actually doing anything? Comment out the "os.system(myKillString)" on line 82 and it will log it's activities, but not kill off the process.
#
# Things to configure:
#
# Line 27: Edit the location of your log file. By default I have it logging to /srv/salt/_scripts/autokill.log so you're going to want to change it.
# Line 42: Edit maxAge (in seconds). By default I'll wait for a process to be older than 1 hour before script takes action
#
#
###


import logging
import json
import os
import sys
import time

logging.basicConfig(stream=sys.stdout, filename='/srv/salt/_scripts/autokill.log',level=logging.DEBUG)

tick = time.asctime( time.localtime(time.time()) )

logging.info(("{} starting run...").format(tick))

try:
    os.remove('/tmp/run.json')
except:
    pass

logging.info(("checking jobs...").format(tick))
os.system('salt-run jobs.active --out json >> /tmp/run.json')


maxAge = 3600 #1 hour

with open('/tmp/run.json') as f:
    data = json.load(f)

for key, value in data.items():
    myKey = key
    myTarget = value['Target']
    myFunction = value['Function']
    myRunning = value['Running'][0]
    myStartTime = value['StartTime']

    keyMyArguments = value['Arguments']

    try:
        keyMyArguments = keyMyArguments[0]
    except:
        pass

    for keyMyRunning, valueMyRunning in myRunning.items():
        keyMyRunning = keyMyRunning

    # make up a default kill string.
    myKillString = "salt '{}' saltutil.kill_job {}".format(keyMyRunning, myKey)

    # get my current time stamp
    myNow = time.time()

    # figure out the epoch in the current string
    stamp = myStartTime.encode('ascii', 'ignore')
    pattern = '%Y, %b %d %H:%M:%S.%f'
    myRun = int(time.mktime(time.strptime(stamp, pattern)))

    # figure out the process age in seconds
    processAge = (int(round(myNow - myRun)))


    if processAge > maxAge:
        logging.warn(("{} {} is larger than {}. KILLING this process").format(tick, processAge, maxAge))
        logging.warn(("{} {} seconds, {} , {} , {} , {}, {}").format(tick, processAge, myKey, keyMyRunning, myFunction, keyMyArguments, myKillString))
        os.system(myKillString)
    else:
        logging.info(("{} Ignoring {}. Process age {} seconds").format(tick,keyMyRunning,processAge))
        pass


logging.info(("{} FINISH run...").format(tick))