#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. "
                "Are you sure it's installed and available on your PYTHONPATH environment variable? "
                "Did you forget to activate a virtual environment?"
            )

        raise

    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, "zanhu"))

    execute_from_command_line(sys.argv)

a = [[1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60],
     [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40],
     [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40],
     [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60],
     [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1],
     [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40],
     [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40],
     [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60],
     [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40], [1, 20, 40], [20, 1, 60], [30, 60, 1], [2, 1, 40]]
