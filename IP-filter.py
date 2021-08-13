# This Python file uses the following encoding: utf-8
import sys
import os
import redis
import re


class IPFilter:
    def __init__(self, logFile, IPFile):
        self.logFile = logFile
        self.IPFile = IPFile
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def checkIP(self):
        f = open(self.IPFile, "r")
        for line in f:
            self.r.setnx(line, "")
        f.close()
        f = open(self.logFile, "r")
        for line in f:
            IPs = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)
            for IP in IPs:
                if self.r.exists(IP+"\x0A"):
                    print("warning: " + line)
                    break
        f.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments passed")
        sys.exit()

    if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
        filter = IPFilter(sys.argv[1], sys.argv[2])
        filter.checkIP()
        del filter
    else:
        print("Files don't exist")
