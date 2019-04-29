#!/usr/bin/python3

import dnf
import subprocess
import tempfile
import json
import jinja2

class Image:
    def __init__(self, image, name=None):
        self.image = image
        self.name = name
        if not self.name:
            self.name = image
        self.packages = []
        self.analyzed = False
        self.size_bytes = 0
    
    def analyze(self):
        base = dnf.Base()

        # Get the image size
        data = subprocess.check_output(['podman', 'inspect', self.image])
        self.size_bytes = json.loads(data)[0]["Size"]

        # Extract DNF and RPM data
        with tempfile.TemporaryDirectory() as tmp:
            cmd = "mkdir -p /workdir/var/lib && cp -r /var/lib/dnf /workdir/var/lib/ && cp -r /var/lib/rpm /workdir/var/lib/"
            subprocess.run(['podman', 'run', '--rm', '-v', tmp+':/workdir:z', '-v', 'copy.sh:/copy.sh:z', self.image, '/bin/sh', '-c', cmd])

            base.conf.installroot = tmp
            base.fill_sack()

        query = base.sack.query()
        installed = list(query.installed())

        pkgs = []

        for pkg in installed:
            pkgs.append(pkg.name)

        self.packages = pkgs
        self.analyzed = True

    def size(self, suffix='B'):
        for unit in ['','K','M']:
            if abs(self.size_bytes) < 1024.0:
                return "%3.1f %s%s" % (self.size_bytes, unit, suffix)
            self.size_bytes /= 1024.0
        return "%.1f %s%s" % (self.size_bytes, 'G', suffix)

    def compare_with_base(self, base):
        in_base = list(set(base.packages) & set(self.packages))
        not_in_base = list(set(self.packages) - set(in_base))

        in_base.sort()
        not_in_base.sort()

        self.pkgs_in_base = in_base
        self.pkgs_not_in_base = not_in_base

def get_template():

    template = """
<style>
.in-base td {
    background-color: #e3ece1;
}
</style>
<table>
    <thead>
        <tr>
            <th></th>
            <th>{{base.name}}</th>
            {% for image in images %}
            <th>{{image.name}}</th>
            {% endfor %}
        </tr>
        <tr>
            <td></td>
            <td>{{base.size()}}</td>
            {% for image in images %}
            <td>{{image.size()}}</td>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
        {% for pkg in base.packages %}
        <tr class="in-base">
            <td>{{pkg}}</td>
            <td>{{pkg}}</td>
            {% for image in images %}
            {% if pkg in image.pkgs_in_base %}
            <td>{{pkg}}</td>
            {% else %}
            <td> - </td>
            {% endif %}
            {% endfor %}
        </tr>
        {% endfor %}
        {% for pkg in extra_pkgs %}
        <tr>
            <td>{{pkg}}</td>
            <td> - </td>
            {% for image in images %}
            {% if pkg in image.packages %}
            <td>{{pkg}}</td>
            {% else %}
            <td> - </td>
            {% endif %}
            {% endfor %}
        </tr>
        {% endfor %}
    </tbody>
</table>
"""
    return template
        

def main():
    names = [
        "fedora-httpd:f29",
        "fedora-mariadb:f29",
        "fedora-nginx:f29",
        "fedora-nodejs:f29",
        "fedora-postgres:f29",
        "fedora-python:f29",
        "scratch-fedora-busybox:f29",
        "scratch-fedora-dnf:f29",
        "scratch-fedora-httpd:f29",
        "scratch-fedora-mariadb:f29",
        "scratch-fedora-microdnf:f29",
        "scratch-fedora-nginx:f29",
        "scratch-fedora-nodejs:f29",
        "scratch-fedora-postgres:f29",
        "scratch-fedora-python:f29",
    ]

    base = Image('fedora:29')
    base.analyze()

    images = []

    for name in names:
        image = Image(name)
        image.analyze()
        image.compare_with_base(base)
        images.append(image)

    # All packages that are not in the base
    extra_pkgs = []
    for image in images:
        extra_pkgs += image.pkgs_not_in_base
    extra_pkgs = list(set(extra_pkgs))
    extra_pkgs.sort()
        

    template = jinja2.Template(get_template())
    print (template.render(base=base, images=images, extra_pkgs=extra_pkgs))
    



if __name__ == "__main__":
    main()



