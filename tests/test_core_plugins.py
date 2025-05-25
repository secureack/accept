import pytest
import os

import core.plugins
import core.functions

def test_load_plugins():
    orig_cwd = os.getcwd()
    if orig_cwd == "/workspace":
      os.chdir("/workspace/accept")
    try:
        core.plugins.load()
        assert "input" in core.plugins.available
        assert "processor" in core.plugins.available
        assert "output" in core.plugins.available

        # Check if at least one plugin of each type is loaded
        assert len(core.plugins.available["input"]) > 0
        assert len(core.plugins.available["processor"]) > 0
        assert len(core.plugins.available["output"]) > 0
        
		# Check if functions are loaded
        assert len(core.functions.available) > 0
    finally:
      if os.getcwd() != orig_cwd:
        os.chdir(orig_cwd)