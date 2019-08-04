from fedora:31 as build-env

run mkdir /output
run dnf -y --installroot /output --releasever 31 install postgresql
run dnf -y --installroot /output --releasever 31 clean all

from scratch
copy --from=build-env /output /
