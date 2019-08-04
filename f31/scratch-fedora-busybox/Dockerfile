from fedora:31 as build-env

run mkdir /output
run dnf -y --installroot /output --releasever 31 install busybox
run dnf -y --installroot /output --releasever 31 clean all

run mkdir /output/bin
run for i in $(/output/sbin/busybox --list); do ln -s /sbin/busybox /output/bin/$i; done

from scratch
copy --from=build-env /output /
