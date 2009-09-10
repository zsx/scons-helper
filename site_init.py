# vim: ft=python expandtab
import subprocess
import re
from SCons.Script import *

def GBuilder(env):
    def dot_in_fun(target, source, env):
            if not env.has_key('DOT_IN_SUBS'):
                    raise Exception("DOT_IN_SUBS is not set in env")
            t = file(target[0].rstr(), 'w')
            s = file(source[0].rstr(), 'r')
            for l in s.readlines():
                    for k, v in env['DOT_IN_SUBS'].items():
                            l = l.replace(k, v)
                    t.write(l)
            t.close()
            s.close()

    dot_in_processor = env.Builder(action= dot_in_fun, src_suffix = '.in')

    env.Append(BUILDERS={'DotIn': dot_in_processor})

    def dot_symbols2def(target, source, env):
            '''
            (echo -e EXPORTS; $(CPP) -P -DINCLUDE_VARIABLES -DINCLUDE_INTERNAL_SYMBOLS -DG_OS_WIN32 -DALL_FILES - <$(srcdir)/gobject.symbols | sed -e '/^$$/d' -e 's/^/	/' -e 's/G_GNUC_[^ ]*//g' | sort) > gobject.def
            '''
            cpp = subprocess.Popen([env['CC']] + Split('/nologo /EP ' + env['DOT_SYMBOLS_FLAGS']) + [str(source[0])], stdout=subprocess.PIPE).communicate()[0]
            lines = cpp.split('\r\n')
            t = file(target[0].rstr(), 'w')
            t.write('EXPORTS\n')
            lines2 = []
            del_GNUC = re.compile('G_GNUC_[^ ]*')
            for line in lines:
                if line == '':
                    continue
                else:
                    line = re.sub(del_GNUC, '', line)
                    line = '    ' + line + '\n'

                lines2.append(line)
            lines2.sort()
            t.writelines(lines2)
            t.close()

    dot_symbols2def_processor = env.Builder(action= dot_symbols2def, src_suffix = '.symbols')

    env.Append(BUILDERS={'DotSymbols2Def': dot_symbols2def_processor})

def Initialize(env):
    if env['DEBUG']:
            print "Debug environment"
            env['DEBUG_CFLAGS'] = '/Od'
            env['DEBUG_CPPDEFINES'] = ['_DEBUG']
            #env['CCPDBFLAGS'] = ['${(PDB and "/Zi /Fd%s" % File(PDB)) or ""}']
            env.Append(CFLAGS = '/MDd')
            env.Append(LIB_SUFFIX = '-msvcrt90d')
    else:
            print "Release environment"
            env['DEBUG_CFLAGS'] = '/Ox'
            env['DEBUG_CPPDEFINES'] = ['_NDEBUG']
            env.Append(CFLAGS = '/MD')
            env.Append(LIB_SUFFIX = '-msvcrt90')

def GInitialize(env):
    Initialize(env)
    if env['DEBUG']:
            env['DEBUG_CPPDEFINES'] = ['G_ENABLE_DEBUG', '_DEBUG']
