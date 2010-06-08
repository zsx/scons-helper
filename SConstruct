# vim: ft=python expandtab
import os
from site_init import GBuilder
opts = Variables()
opts.Add(PathVariable('PREFIX', 'InstallDevation prefix', os.path.expanduser('~/FOSS'), PathVariable.PathIsDirCreate))
env = Environment(variables = opts, ENV=os.environ, tools = ['default', GBuilder])
env.Tool('wixtool', '#')
all_libs = {'zlib': [],
            'pixman': [],
            'intl':[],
            'winiconv':[],
            'png': ['zlib'],
            'libxml2':['zlib'],
            'dbus': ['libxml2'],
            'glib': ['zlib', 'winiconv', 'intl'],
            'gmodule': ['glib'],
            'gthread': ['glib'],
            'gobject': ['glib', 'gthread'],
            'dbus-glib': ['dbus', 'gobject'],
            'gio':['glib', 'gobject', 'gmodule']}
dev_libs = all_libs.copy()
run_libs = all_libs.copy()
del run_libs['pixman']
libs = {'Run': run_libs,
        'Dev': dev_libs}
all_apps = {}
dev_apps = all_apps.copy()
run_apps = all_apps.copy()
apps = {'Run': run_apps,
        'Dev': dev_apps}

dev_modules = dict(dev_libs.items() + dev_apps.items())
run_modules = dict(run_libs.items() + run_apps.items())

modules = {'Run': run_modules,
           'Dev': dev_modules}
for f in ['Run', 'Dev']:
    for m in modules[f]:
        s = env['PREFIX'] + r'\\wxs\\%s%s.wxs' % (m, f)
        env.WiX('%s%s.msm'% (m, f), s)

def generate_featuregroup_dependency(modules, flavor):
    ret = ''
    for k in modules.keys():
        ret += '''<FeatureGroup Id='%s%sGroup'>
            <MergeRef Id='%s%s' />\n'''% (k.replace('-', '_').title(), flavor, k.replace('-', '_').title(), flavor)
        if modules[k]:
            for d in modules[k]:
                ret += '''<FeatureGroupRef Id='%s%sGroup' />\n'''% (d.replace('-', '_').title(), flavor)
        ret += '</FeatureGroup>\n'
    return ret
def generate_merge(modules, flavor):
    ret = ''
    for m in modules.keys():
        ret += "<Merge Id='%s%s' Language='1033' SourceFile='%s%s.msm' DiskId='1' />\n" % (m.replace('-', '_').title(), f, m, f.lower())
    return ret

def generate_feature_ref(modules, flavor):
    ret = ''
    k = [m for m in modules.keys()]
    k.sort()
    for m in k:
        ret += """<Feature Id='%s' Title='%s' Description='Install %s and its dependencies' Display='expand' Level='1'>
        <FeatureGroupRef Id='%s%sGroup' />
        </Feature>\n""" % (m.replace('-', '_').title(), m.title(), m, m.replace('-', '_').title(), flavor)
    return ret

for f in ['Run', 'Dev']:
    env_dep = env.Clone()
    env_dep['DOT_IN_SUBS'] = {'@FLAVOR@': f,
                              '@FEATURE_GROUPS@': generate_featuregroup_dependency(modules[f], f)}
    env_dep.DotIn('Dependency%s.wxs' % f, 'Dependency.wxs.in')
    env_dep.Depends('Dependency%s.wxs' % f, 'SConstruct')

    e = env.Clone()
                        
    e['DOT_IN_SUBS'] = {'@VERSION@': '0.0.0.2',
                        '@MERGE_MODULES@': generate_merge(modules[f], f),
                        '@FEATURE_LIBS@': generate_feature_ref(libs[f], f),
                        '@FEATURE_APPS@' : generate_feature_ref(apps[f], f)}
    e.DotIn('Gnome4Win%s.wxs' % f, 'Gnome4Win%s.wxs.in' % f)
    e.Depends('Gnome4Win%s.wxs' % f, 'SConstruct')
    e.Append(WIXLIGHTFLAGS = ['-ext', 'WixUIExtension'])
    sources = ['Gnome4Win%s.wxs' % f, 'Dependency%s.wxs' % f]
    e.WiX('Gnome4Win%s.msi' % f, sources)
    e.Depends('Gnome4Win%s.msi' % f, [x+ f.lower() + '.msm' for x in modules[f].keys()])

