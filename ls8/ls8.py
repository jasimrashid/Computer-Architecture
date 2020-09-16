#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

# cpu.load('examples/print8.ls8')
cpu.load('examples/mult.ls8')
cpu.run()