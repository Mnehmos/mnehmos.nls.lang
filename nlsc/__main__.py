"""
Entry point for running nlsc as a module: python -m nlsc
"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
