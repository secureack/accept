import pytest
import os

import core.plugins
import core.functions

def test_load_plugins():
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