from fedora:29 as build-env

run mkdir /output
run dnf -y --installroot /output --releasever 29 install nginx
run dnf -y --installroot /output --releasever 29 clean all

from scratch
copy --from=build-env /output /
