#!/usr/bin/env python

import os
import shutil
import subprocess
import sys

from util import *

def main(args):
  script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
  base_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
  os.chdir(base_dir)

  build_dir = os.path.join(base_dir, "build")

  # Generate project files
  subprocess.call([
    "./tools/gyp/gyp",
    "hello.gyp",
    "--depth=.",
    "--generator-output=build",
  ])

  if is_mac():
    # Switch to build folder (since that's what Xcode expects)
    os.chdir(build_dir)

    # Build project
    subprocess.call([
      "xcodebuild",
      "-Dmodule_root_dir=" + os.getcwd(),
      "-target=hello",
      "-configuration=Debug",
      "-destination=build",
    ])

if __name__ == "__main__":
  main(sys.argv)
