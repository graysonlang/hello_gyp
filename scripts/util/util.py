#!/usr/bin/env python

import platform

def is_mac():
  return platform.system() == "Darwin"

def is_win():
  return platform.system() == "Windows"
