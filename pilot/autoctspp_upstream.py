"""Run a released script of the upstream tree unchanged, with shims for names that newer library versions removed.

    python -m pilot.autoctspp_upstream <script.py> <its arguments>
"""
import os
import runpy
import sys

import numpy as np
import pandas as pd

if not hasattr(pd.DatetimeIndex, "weekofyear"):                      # removed in pandas 2.0
    pd.DatetimeIndex.weekofyear = property(lambda s: pd.Index(s.isocalendar().week.to_numpy().astype("int64")))
for _name, _type in (("float", float), ("int", int), ("bool", bool), ("object", object)):   # removed in numpy 1.24
    if _name not in np.__dict__:
        setattr(np, _name, _type)

if __name__ == "__main__":
    script = sys.argv[1]
    sys.argv = sys.argv[1:]
    sys.path.insert(0, os.path.dirname(os.path.abspath(script)))    # what "python script.py" does
    runpy.run_path(script, run_name="__main__")
