# autokill for Saltstack.

This script will run and kill off any hung up Salt jobs which may be lingering on your salt master server. The goal of this script is to keep the number of stuck processes from overloading your salt-master. 

I work in a "highly dynamic" environment which can cause issues with minions reporting back promptly. To keep things sane on my salt-master, I generally terminate any jobs taking over an hour to complete. It's been running on my 2018.3.0 (Oxygen) salt master for 1+ years without an issue.

Want to see it work without actually doing anything? Comment out the `os.system(myKillString)` on line 82 and it will log it's activities, but not kill off the process.

Things to configure:

* Line 27: Edit the location of your log file. By default I have it logging to `/srv/salt/_scripts/autokill.log` so you're going to want to change it.
* Line 42: Edit `maxAge` (in seconds). By default I'll wait for a process to be older than 1 hour before script takes action, but your environment may be different.

Enjoy!

tom