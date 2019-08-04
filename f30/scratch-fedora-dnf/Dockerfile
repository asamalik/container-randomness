from fedora:30 as build-env

run mkdir /output
run dnf -y --installroot /output --releasever 30 install dnf
run dnf -y --installroot /output --releasever 30 clean all

from scratch
copy --from=build-env /output /
