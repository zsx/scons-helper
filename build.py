#!/usr/bin/python
# vim: ft=python expandtab

import subprocess
import os
import sys

top_dir = os.path.abspath(os.path.dirname(__file__))

packs = ['zlib',
         'pixman',
         'png',
         'jpeg-7',
         'freetype2',
         'glib',
         'libxml2',
         'fontconfig',
         'cairo',
         'atk', 
         'pango',
         'gtk',
         'librsvg', 
         'poppler',
         'evince'
         ]

def build():
    action = "Install"
    log = file('build.log', 'w')
    if len(sys.argv) > 1 and ('-c' in sys.argv[1:] or '--clean' in sys.argv[1:]):
        packs.reverse()
        action = "Uninstall"
    for p in packs:
        args = [r'--site-dir=..', r'PREFIX=C:\FOSS\Debug', 'DEBUG=1', r'PERL=C:\Perl\bin\perl.exe'] + sys.argv[1:]
        os.chdir(p)
        '''
        print "Building ", p,
        ret = subprocess.Popen(['scons'] + args, shell=True, stdout = log).wait()
        if not ret:
            print ": Success"
        else:
            print ": Failure"
            log.close()
            return
        '''

        if p in ['pango']:
            args += [r'--install-sandbox=C:\FOSS\debug']
        print action + 'ing ', p,
        ret = subprocess.Popen(['scons'] + args + ['install'], shell=True, stdout = log).wait()
        if not ret:
            print ": Success"
        else:
            print ": Failure"
            log.close()
            return
        os.chdir(top_dir)
    log.close()


if __name__ == '__main__':
    build()
