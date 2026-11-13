# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:52:08 2026

@author: adamb
"""


    
import ctypes
import importlib.util
from pathlib import Path

# Locate MediaPipe
spec = importlib.util.find_spec("mediapipe")

folder = Path(spec.submodule_search_locations[0])

print("MediaPipe folder:", folder)

# Find MediaPipe native libraries
files = list(folder.rglob("*.dll"))
files += list(folder.rglob("*.pyd"))

print("Native libraries found:", len(files))

for file in files:
    print("\nTesting:", file)

    try:
        ctypes.CDLL(str(file))
        print("Loaded successfully")

    except OSError as error:
        print("FAILED:", error)    