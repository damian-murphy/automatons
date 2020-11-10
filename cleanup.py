#!/usr/bin/python
#  Copyright (c) 2020 damian@orchestrating-automatons.eu
# Furthering my Learning Python series, I now try to manage my backups
#
import os, time

backups = "/backup.dir"
today = time.time()
count = 0
retention_days = 7

for f in os.listdir(backups):
    fpath = os.path.join(backups, f)
    if os.stat(fpath).st_mtime < today - retention_days * 86400:
        if os.path.isfile(fpath):
            print("Found " + f + ", which is about " + str( round((today - os.stat(fpath).st_mtime) / 86400) ) + " days old, deleting.")
            os.remove(os.path.join(fpath))
            count = count + 1

print("Done - removed " + str(count) + " files, hopefully that's what was desired.")
print("0 OK, 0:1")
