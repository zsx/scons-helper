# vim: set ft=python
import os

env = Environment()

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
prefix=os.path.expanduser(r'~\FOSS\Debug')

if ARGUMENTS.get('debug', 0):
	print "Debug environment"
	env.Append(CCPPDEFINES = '_DEBUG')
	env.Append(CFLAGS = '/Od')
	env['CCPDBFLAGS'] = ['${(PDB and "/Zi /Fd%s" % File(PDB)) or ""}']
	env.Append(LIB_SUFFIX = '-msvcrt90d')
	prefix=os.path.expanduser(r'~\FOSS\Debug')
else:
	print "Release environment"
	env.Append(CFLAGS = '-Ox')
	env.Append(LIB_SUFFIX = '-msvcrt90')
	prefix=os.path.expanduser(r'~\FOSS\Release')

SConscript(['zlib/SConscript',
			'pixman/SConscript'], 
			exports='env prefix')
