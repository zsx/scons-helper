#!/bin/sh
GNOME_MODULES="gtk pango atk glib libxml2 librsvg gmime totem-plparser totem evince"
FREEDESKTOP_MODULES="cairo pixman poppler"
MODULES_WITH_UPSTREAM=("png")
MODULES_UPSTREAM=("git://libpng.git.sourceforge.net/gitroot/libpng/libpng")
OTHER_MODULES="freetype"
ALL_MODULES="$GNOME_MODULES $FREEDESKTOP_MODULES $MODULES_WITH_UPSTREAM $OTHER_MODULES"
for mod in $ALL_MODULES
do 
	git clone git@github.com:zsx/$mod.git
	cd $mod
	echo "rename $mod's origin to github" 
	git remote rename origin github
	git branch scons --track github/scons
	git checkout scons
	cd ..
done

add_origin()
{
#add_origin mod origin
	cd $1
	echo "adding $1's origin"
	echo $2
	git remote add origin $2
   	cd ..
}

add_origin_root() 
{
#add_origin_root mod root
	add_origin $1 $2/$1
}
for mod in $GNOME_MODULES
do 
	add_origin_root $mod git://git.gnome.org 
done

for mod in $FREEDESKTOP_MODULES
do 
	add_origin_root $mode git://anongit.freedesktop.org/git
done

for ((i = 0; i < ${#MODULES_WITH_UPSTREAM[@]}; i++))
do
	add_origin ${MODULES_WITH_UPSTREAM[$i]} ${MODULES_UPSTREAM[$i]}
done

#git submodule init
