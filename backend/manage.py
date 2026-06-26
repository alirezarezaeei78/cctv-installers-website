#!/usr/bin/env python
"""
Utility script for running administrative tasks for the Django project.

This file exposes the ``main`` function for Django’s command‑line utility.
It sets up the default settings module and executes management commands.

The project is configured to be run locally with SQLite and includes
support for the Django admin as well as a simple REST API. When deployed
elsewhere, the ``DJANGO_SETTINGS_MODULE`` environment variable may be
overridden to point at alternative configurations.
"""
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your "
            "PYTHONPATH environment variable? Did you forget to activate a virtual "
            "environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()