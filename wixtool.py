"""
Tool to support WiX (Windows Installer XML toolset)
http://blogs.msdn.com/robmen/
http://sourceforge.net/projects/wix
"""
__revision__ = "$Revision: 1.1 $"
__date__ = "$Date: 2004/05/21 20:44:46 $"
__author__ = "elliot.murphy@veritas.com"
__credits__ = ""

import os
import xml.sax

import SCons.Defaults
import SCons.Util
import SCons.Scanner

def wix_scanner(node, env, path):
    ext = os.path.splitext(str(node))[1]
    known_wix_sourcefiles = ['.wxs', '.wxi']
    if ext not in known_wix_sourcefiles:
        return []

    include_files = []
    other_deps = []

    class MyHandler(xml.sax.handler.ContentHandler):

        def processingInstruction(self, target, data):
            if target == 'include':
                data = str(data.strip())
                if data not in include_files:
                    include_files.append(data)

        def startElement(self, name, attrs):
            # EJM - Not sure about the Directory and DirectoryRef elements. They
            # both have src attributes, but I don't know enough about MSI to
            # decide # if that means they should contribute to our dependency
            # graph. For now, they are not included.
            #
            # Not sure about the SFPCatalog element. I don't think groups
            # outside of MS will need to update the SFP catalog, so it's probably
            # safe to ignore for now. If someone from MS starts using this,
            # please update accordingly
            element_names = [
                'File',
                'Merge',
                'Binary',
                'Icon',
                'DigitalCertificate',
                'DigitalSignature',
                'FileGroup',
                'Text'
                ]

            if name in element_names:
                names = attrs.getNames()
                if 'src' in names:
                    src = str(attrs.getValue('src'))

                    # This part is a bit of a hack for handling relative paths
                    # in both WiX and SCons. If the src attribute in the WiX
                    # file contains a directory separator, we assume that it
                    # is supposed to be a relative path from the root of the
                    # source tree, not from the directory that the Sconscript
                    # file is in. In order to do this, we prepend the magic #
                    # to the path so that scons will know the path is relative
                    # to the source tree root. The WiX compiler and linker are
                    # invoked from the root of the source tree, so they already
                    # treat src attributes as relative to the root of the src
                    # tree.
                    if '/' in src:
                        src = '#' + src

                    if src not in other_deps:
                        other_deps.append(src)

    xml.sax.parseString(node.get_contents(), MyHandler())
    print include_files, other_deps
    return include_files + other_deps

def generate(env):
    """Add Builders and construction variables for WiX to an Environment."""
    env['WIXCANDLE'] = 'candle.exe'
    env['WIXCANDLEFLAGS'] += ['-nologo']
    env['WIXCANDLEINCLUDE'] = []
    env['WIXCANDLECOM'] = '$WIXCANDLE $WIXCANDLEFLAGS -I $WIXCANDLEINCLUDE -o ${TARGET} ${SOURCE}'

    env['WIXLIGHT'] = 'light.exe'
    env['WIXLIGHTFLAGS'] = ['-nologo']
    env['WIXLIGHTCOM'] = "$WIXLIGHT $WIXLIGHTFLAGS -out ${TARGET} ${SOURCES}"

    wxi_scanner = env.Scanner(
        function = wix_scanner,
        name = 'WiX Scanner',
        skeys = ['.wxs', '.wxi'],
        recursive = 1)

    env['SCANNERS'] += [wxi_scanner]

    object_builder = SCons.Builder.Builder(
        action = '$WIXCANDLECOM',
        suffix = '.wixobj',
        src_suffix = '.wxs')

    linker_builder = SCons.Builder.Builder(
        action = '$WIXLIGHTCOM',
        src_suffix = '.wixobj',
        src_builder = object_builder)

    env['BUILDERS']['WiX'] = linker_builder

def exists(env):
    return 1 # TODO: Should we do a better job of detecting?

