from fedora:32 as build-env

run mkdir /output
run dnf -y --installroot /output --releasever 31 --no-docs --setopt=install_weak_deps=False install httpd glibc-minimal-langpack coreutils-single 
run dnf -y --installroot /output --releasever 31 clean all

from scratch
copy --from=build-env /output /
