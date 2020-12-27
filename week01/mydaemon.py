#!/usr/bin/env python3
# coding=utf-8

import os
import sys
import time
import datetime
import random
import pathlib

# daemon server
def recordtime():
    # recording
    sys.stdout.write("daemon[{}] is recording log\n".format(os.getpid()))
    # for system feature
    num = random.randint(10, 20)
    while num > 0:
        # proc for loop
        # get current time and print
        sys.stdout.write("{}: doing something...\n".format(time.asctime(time.localtime())))
        sys.stdout.flush()
        time.sleep(4)

def generatefilenamewithdir(filename="/usr/log/python-1700-1-1/mydaemon.py"):
    # get string of date
    date = "python-" + datetime.date.today().isoformat()
    # generate dir
    newdir = pathlib.Path(filename).parents[1].joinpath(date)
    # create dir
    if True != pathlib.Path(newdir).is_dir():
        pathlib.Path(newdir).mkdir(parents=True)
    # get filename
    newfilename = pathlib.Path(filename).name
    # generate new filename
    return pathlib.Path(newdir).joinpath(newfilename)

# create daemon process
def mydaemon(stdin="/dev/null", stdout="/dev/null", stderr="/dev/null"):
    print("daemon process starting...")
    try:
        # create first subprocess
        pid = os.fork()
        # first prarent process
        if pid > 0:
            print("first parent process exit")
            exit(0)
    # for error
    except OSError as oserr:
        sys.strerr.write("create first subprocess failed, reason: {}\n".format(oserr))
        sys.exit(1)
    
    # config env
    os.chdir("/")
    os.umask(0)
    os.setsid()

    try:
        # create second subprocess // daemon
        pid = os.fork()
        if pid > 0:
            print("second parent process exit")
            exit(0)
    except OSError as oserr:
        sys.strerr.write("create subprocess failed, reason: {}\n".format(oserr))
        sys.exit(1)

    # notify daemon is runging
    sys.stdout.write("daemon[{}] runing...\n".format(os.getpid()))

    # clean buffer
    sys.stdout.flush()
    sys.stderr.flush()

    # generate filename with dir
    stdout = generatefilenamewithdir(stdout)

    # create new fd
    newin = open(stdin,"r")
    newout = open(stdout, "a+")
    newerr = open(stderr, "w")

    # close old fd, and cp form new fd
    os.dup2(newin.fileno(), sys.stdin.fileno())
    os.dup2(newout.fileno(), sys.stdout.fileno())
    os.dup2(newerr.fileno(), sys.stderr.fileno())

    # daemon server
    recordtime()


if __name__ == "__main__":
    mydaemon("/dev/null", "/var/log/python-1700-1-1/mydaemon.log", "/dev/null")
