# vim: ft=python expandtab
import subprocess
import re
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
        if not (env.has_key('GLIB_GENMARSHAL_ARGV')
                and env.has_key('GLIB_GENMARSHAL')):
            raise Exception("set GLIB_GENMARSHAL_ARGV before gen_marshal")
        args = [env['GLIB_GENMARSHAL']]
        for arg in env['GLIB_GENMARSHAL_ARGV']:
            if (isinstance(arg, tuple) or isinstance(arg, list)) \
                and len(arg) == 2:
                args.append('--%s=%s' % (arg[0], arg[1]))
            else:
                args.append('--%s' % arg)
        args += map(str, source)
        fd, fp = mkstemp()
        os.close(fd)
        try:
            for t in target:
                tpath = str(t)
                fo = file(fp, 'w')
                if tpath.endswith('.h'):
                    subprocess.Popen(' '.join(args + ['--header']), stdout = fo).wait()
                if tpath.endswith('.c'):
                    subprocess.Popen(' '.join(args + ['--body']), stdout = fo).wait()
                fo.close()
                if os.path.exists(tpath) and cmp(fp, tpath):
                    continue
                else:
                    copyfile(fp, tpath) #target will be replaced
        finally:
            os.unlink(fp)

    marshal_generator = env.Builder(action = gen_marshal, src_suffix = '.list')
    env.Append(BUILDERS={'MarshalGenerator': marshal_generator})

    def mkenums(target, source, env):
        if not (env.has_key('GLIB_MKENUMS_ARGV')
                and env.has_key('GLIB_MKENUMS')):
            raise Exception("set GLIB_MKENUMS_ARGV before gen_marshal")
        tpath = str(target[0])
        args = [env['PERL'], env['GLIB_MKENUMS']]
        for arg in env['GLIB_MKENUMS_ARGV']:
            if (isinstance(arg, tuple) or isinstance(arg, list))\
                and len(arg) == 2:
                args.append('--%s %s' % (arg[0], arg[1]))
            else:
                args.append('--%s' % argv)
        args += map(str, source)
        fd, fp = mkstemp()
        try:
            fo = os.fdopen(fd, 'w')
            subprocess.Popen(' '.join(args), stdout = fo).wait()
            fo.close()
            if not os.path.exists(tpath) or not cmp(fp, tpath):
                copyfile(fp, tpath) #target will be replaced
        finally:
            os.unlink(fp)

    mkenums_generator = env.Builder(action = mkenums, src_suffix = '.h')
    env.Append(BUILDERS={'MkenumsGenerator': mkenums_generator})

def Initialize(env):
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
        env['DEBUG_CPPDEFINES'] = ['G_ENABLE_DEBUG', '_DEBUG']
