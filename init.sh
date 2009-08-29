#!/bin/sh
GNOME_MODULES="gtk pango atk glib libxml2 totem-plparser totem"
CAIRO_MODULES="cairo pixman"
OTHER_MODULES="png"
ALL_MODULES="$GNOME_MODULES $CAIRO_MODULES $OTHER_MODULES"
for mod in $ALL_MODULES
do 
	cd $mod
	echo "rename $mod's origin to github" 
	git remote rename origin github
	git branch OAH --track github/OAH
	git checkout OAH
	cd ..
done

for mod in $GNOME_MODULES
do 
	cd $mod
	echo "adding $mod's origin"
	git remote add origin git://git.gnome.org/$mod
   	cd ..
done

for mod in $CAIRO_MODULES
do 
	cd $mod
	echo "adding $mod's origin"
	git remote add origin git://anongit.freedesktop.org/git/$mod
   	cd ..
done

cd png
echo "adding png's origin"
git remote add origin git://libpng.git.sourceforge.net/gitroot/libpng 
cd ..

git submodule init
