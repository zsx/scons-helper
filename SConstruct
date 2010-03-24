# vim: ft=python expandtab
env = Environment()
env.Tool('wixtool', '#')
modules=['zlib/zlibrun.msm',
         'zlib/zlibdev.msm']
env.Append(WIXLIGHTFLAGS = ['-ext', 'WixUIExtension'])

env.WiX('Gnome4Win.msi', ['Gnome4Win.wxs', 'dependency.wxs'])
env.Depends('Gnome4Win.msi', modules)
