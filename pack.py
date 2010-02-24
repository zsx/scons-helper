# vim: ft=python expandtab
import zipfile
import re, os
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-r", "--root", dest="root",
                  help="The root of the package directory", metavar="DIR")
parser.add_option("-n", "--package-name", dest="pack_name",
                  help="The name to the package to be packed", metavar="NAME")
parser.add_option("-p", "--package-dir", dest="pack_dir",
                  help="The path to the package to be packed", metavar="DIR")
parser.add_option("-v", "--version", dest="version", default="",
                  help="The version append to the zip file")

(options, args) = parser.parse_args()

if not options.pack_dir.endswith('/'):
    options.pack_dir += '/'
manifest = open(options.pack_dir + options.pack_name + '_MANIFEST.txt', 'r')
ver = ""
for x in manifest.readlines():
    o = re.compile(R'^@VER@(.*)$').match(x)
    if o:
        ver = o.group(1)
        break
pack_name = options.pack_name
if ver != "":
    pack_name += '-' + ver
if options.version != "":
    pack_name += '-' + options.version[:6]

zfr = zipfile.ZipFile(options.pack_dir + pack_name + '-run.zip', 'w')
zfd = zipfile.ZipFile(options.pack_dir + pack_name + '-dev.zip', 'w')

manifest.seek(0, os.SEEK_SET)
for x in manifest.readlines():
    x = x.rstrip('\n')
    #print "x = ", x
    r = re.compile(r'^@RUN@(.*)$').match(x)
    if r:
        #print "putting %s into run as %s" % (r.group(1), r.group(1)[len(options.root):])
        zfr.write(r.group(1), r.group(1)[len(options.root):])
    d = re.compile(r'^@DEV@(.*)$').match(x)
    if d:
        #print "putting %s in to dev" % d.group(1)
        zfd.write(d.group(1), d.group(1)[len(options.root):])
    a = re.compile(r'^@ANY@(.*)$').match(x)
    if a:
        #print "putting %s in to both" % a.group(1)
        zfr.write(a.group(1), a.group(1)[len(options.root):])
        zfd.write(a.group(1), a.group(1)[len(options.root):])

zfr.close()
zfd.close()

manifest.close()
