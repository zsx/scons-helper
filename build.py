#!/usr/bin/python
# vim: ft=python expandtab

import subprocess
import os
import sys

top_dir = os.path.dirname(__file__)

packs = ['zlib',
         'pixman',
         'png',
         'cairo',
         'glib']

args = [r'--site-dir=..', r'PREFIX=C:\FOSS\Debug', 'DEBUG=1', r'PERL=C:\Perl\bin\perl.exe', 'build_test=1'] + sys.argv[1:]

def build():
    log = file('build.log', 'w')
    for p in packs:
        os.chdir(p)
        print "Building ", p,
        ret = subprocess.Popen(['scons'] + args, shell=True, stdout = log).wait()
        if not ret:
            print ": Success"
        else:
            print ": Failure"

        print "Installing ", p,
        ret = subprocess.Popen(['scons'] + args + ['install'], shell=True, stdout = log).wait()
        if not ret:
            print ": Success"
        else:
            print ": Failure"
        os.chdir(top_dir)
    log.close()


if __name__ == '__main__':
    build()
