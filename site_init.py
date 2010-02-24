# vim: ft=python expandtab
import subprocess
import re
import os
from filecmp import cmp
from tempfile import mkstemp
from shutil import copyfile
from SCons.Script import *

def GBuilder(env):
    def dot_in_fun(target, source, env):
        if not env.has_key('DOT_IN_SUBS'):
            raise Exception("DOT_IN_SUBS is not set in env")
        t = file(target[0].rstr(), 'w')
        s = file(source[0].rstr(), 'r')
        var = re.compile(r'(@\w+?@)')
        for l in s.readlines():
            mo = var.findall(l)
            if mo:
                for v in mo:
                    if env['DOT_IN_SUBS'].has_key(v):
                        l = l.replace(v, env['DOT_IN_SUBS'][v])
                    else:
                        l = l.replace(v, '')
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

    def gen_marshal(target, source, env):
        if not env.has_key('GLIB_GENMARSHAL_ARGV'):
            raise Exception("set GLIB_GENMARSHAL_ARGV before gen_marshal")
        if env.has_key('GLIB_GENMARSHAL'):
            args = [env['GLIB_GENMARSHAL']]
        elif env['ENV'].has_key('GLIB_GENMARSHAL'):
            args = [env['ENV']['GLIB_GENMARSHAL']]
        else:
            args = [env['PREFIX'] + r'\bin\glib-genmarshal.exe']

        for arg in env['GLIB_GENMARSHAL_ARGV']:
            if (isinstance(arg, tuple) or isinstance(arg, list)) \
                and len(arg) == 2:
                args.append('--%s=%s' % (arg[0], arg[1]))
            else:
                args.append('--%s' % arg)
        args += map(str, source)

        for t in target:
            tpath = str(t)
            fo = file(tpath, 'w')
            if tpath.endswith('.h'):
                subprocess.Popen(' '.join(args + ['--header']), stdout = fo).wait()
            elif tpath.endswith('.c'):
                subprocess.Popen(' '.join(args + ['--body']), stdout = fo).wait()
            fo.close()

    marshal_generator = env.Builder(action = gen_marshal, src_suffix = '.list')
    env.Append(BUILDERS={'MarshalGenerator': marshal_generator})

    def mkenums(target, source, env):
        if not env.has_key('GLIB_MKENUMS_ARGV'):
            raise Exception("set GLIB_MKENUMS_ARGV before gen_marshal")
        tpath = str(target[0])
        if env.has_key('GLIB_MKENUMS'):
            args = [env['PERL'], env['GLIB_MKENUMS']]
        elif env['ENV'].has_key('GLIB_MKENUMS'):
            args = [env['PERL'], env['ENV']['GLIB_MKENUMS']]
        else:
            args = [env['PERL'], env['PREFIX'] + r'\bin\glib-mkenums']
        for arg in env['GLIB_MKENUMS_ARGV']:
            if (isinstance(arg, tuple) or isinstance(arg, list))\
                and len(arg) == 2:
                args.append('--%s %s' % (arg[0], arg[1]))
            else:
                args.append('--%s' % arg)

        args += map(str, source)
        fo = file(tpath, 'w')
        subprocess.Popen(' '.join(args), stdout = fo).wait()
        fo.close()

    mkenums_generator = env.Builder(action = mkenums, src_suffix = '.h')
    env.Append(BUILDERS={'MkenumsGenerator': mkenums_generator})


def __Install(target, source, env, d):
    dest = re.sub(r'\$(\w+)', lambda x: env[x.group(1)], target)
    dest = dest.replace('\\', '/')
    if 'PARENT_ENV' in env:
        __Install(dest, source, env['PARENT_ENV'], d)
        return

    if not dest.endswith('/'):
        dest += '/'
    print "dest = ", dest
    if isinstance(source, str):
        l = [dest + os.path.basename(source)]
    else:
        print "Non str: src = ", source
        l = map(lambda x: dest + os.path.basename(x), source)
    if d not in env:
        env[d] = l
    else:
        env[d] += l
    print "env[%s] = " % d, l
    env.Alias('install', env.Install(target, source))

def InstallRun(target, source, env):
    __Install(target, source, env, "INSTALL_RUNTIME")

def InstallDev(target, source, env):
    __Install(target, source, env, "INSTALL_DEV")

def InstallAny(target, source, env):
    __Install(target, source, env, "INSTALL_ANY")

def __InstallAs(target, source, env, d):
    dest = re.sub(r'\$(\w+)', lambda x: env[x.group(1)], target)
    dest = dest.replace('\\', '/')
    if 'PARENT_ENV' in env:
        __InstallAs(dest, source, env['PARENT_ENV'], d)
    else:
        if d not in env:
            env[d] = [dest]
        else:
            env[d] += [dest]
        env.Alias('install', env.InstallAs(target, source))

def InstallRunAs(target, source, env):
    __InstallAs(target, source, env, "INSTALL_RUNTIME")

def InstallDevAs(target, source, env):
    __InstallAs(target, source, env, "INSTALL_DEV")

def InstallAnyAs(target, source, env):
    __InstallAs(target, source, env, "INSTALL_ANY")

def DumpInstalledFiles(env):
    if 'PACKAGE_NAME' not in env:
        raise Exception("PACKAGE_NAME is not set")
    of = file(env['PACKAGE_NAME'] + '_MANIFEST.txt', 'w')
    print "writing to ", env['PACKAGE_NAME'] + '_MANIFEST.txt'

    if 'PACKAGE_VERSION' in env:
        of.writelines('@VER@' + env['PACKAGE_VERSION'] + '\n')

    if 'PACKAGE_DEPENDS' in env:
        of.writelines('@DEP@' + ','.join(env['PACKAGE_DEPENDS']) + '\n')

    if 'INSTALL_RUNTIME' in env:
        print "Writing INSTALL_RUNTIME:"
        print env['INSTALL_RUNTIME']
        of.writelines(map(lambda x: '@RUN@' + x + '\n', env['INSTALL_RUNTIME']))

    if 'INSTALL_DEV' in env:
        print "Writing INSTALL_DEV:"
        print env['INSTALL_DEV']
        of.writelines(map(lambda x: '@DEV@' + x + '\n', env['INSTALL_DEV']))

    if 'INSTALL_ANY' in env:
        of.writelines(map(lambda x: '@ANY@' + x + '\n', env['INSTALL_ANY']))
    of.close()

def Initialize(env):
    env.AppendENVPath('PKG_CONFIG_PATH', env['PREFIX'] + '/lib/pkgconfig')
    if env['DEBUG']:
        print "Debug environment"
        env['DEBUG_CFLAGS'] = '/Od'
        env['DEBUG_CPPDEFINES'] = ['_DEBUG']
        #env['CCPDBFLAGS'] = ['${(PDB and "/Zi /Fd%s" % File(PDB)) or ""}']
        env.Append(CFLAGS = '/MDd')
        env['LIB_SUFFIX'] = '-msvcrt90d'
    else:
        print "Release environment"
        env['DEBUG_CFLAGS'] = '/Ox'
        env['DEBUG_CPPDEFINES'] = ['_NDEBUG']
        env.Append(CFLAGS = '/MD')
        env['LIB_SUFFIX'] = '-msvcrt90'

def GInitialize(env):
    Initialize(env)
    if env['DEBUG']:
        env['DEBUG_CPPDEFINES'] += ['G_ENABLE_DEBUG']
