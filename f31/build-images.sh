#!/usr/bin/sh

root=$(pwd)

for img in $(ls -d fedora-* scratch-*); do
    name="asamalik/$img:f31"

    cd $img
    podman build -t $name .
    
    cd $root
done
