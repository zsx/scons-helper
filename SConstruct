# vim: ft=python expandtab
env = Environment()
env.Tool('wixtool', '#')
run_modules=['zlib/zlibrun.msm']
dev_modules = [x.replace('run.msm', 'dev.msm') for x in run_modules]
env.Append(WIXLIGHTFLAGS = ['-ext', 'WixUIExtension'])

env.WiX('Gnome4WinRun.msi', ['Gnome4WinRun.wxs', 'DependencyRun.wxs'])
env.WiX('Gnome4WinDev.msi', ['Gnome4WinDev.wxs', 'DependencyDev.wxs'])
env.Depends('Gnome4WinRun.msi', run_modules)
env.Depends('Gnome4WinDev.msi', run_modules)
