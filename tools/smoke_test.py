"""Compatibility entry point for the current campaign engine regression."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('campaign_smoke_test.py')),run_name='__main__')
