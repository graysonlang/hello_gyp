#!/usr/bin/env python3

import sys

script = "./scripts/build.py"

# Add scripts folder to python search path.
sys.path.append("scripts")
sys.argv = [script] + sys.argv[1:]

# Call build script file.
exec(open(script).read())
