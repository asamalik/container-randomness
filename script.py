#!/usr/bin/python3

import dnf
import subprocess
import tempfile

class Installation:
    def __init__(self, container, name=None):
        self.container = container
        self.name = name
        if not self.name:
            self.name = container
        self.packages = []
        self.analyzed = False
    
    def analyze(self):
        base = dnf.Base()

        # Extract DNF and RPM data
        with tempfile.TemporaryDirectory() as tmp:
            cmd = "mkdir -p /workdir/var/lib && cp -r /var/lib/dnf /workdir/var/lib/ && cp -r /var/lib/rpm /workdir/var/lib/"
            subprocess.run(['podman', 'run', '--rm', '-v', tmp+':/workdir:z', '-v', 'copy.sh:/copy.sh:z', self.container, '/bin/sh', '-c', cmd])

            base.conf.installroot = tmp
            base.fill_sack()

        query = base.sack.query()
        installed = list(query.installed())

        pkgs = []

        for pkg in installed:
            pkgs.append(pkg.name)

        self.packages = pkgs
        self.analyzed = True


#Example:
#container = Installation("fedora:29")
#container.analyze()
#for pkg in container.packages:
#    print pkg.name



