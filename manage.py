#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import re


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "compute.settings")
    try:
        with open('/etc/systemd/compute_environment.conf') as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)
    execute_from_command_line(sys.argv)