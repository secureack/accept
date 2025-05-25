import pytest

import core.parser

def test_yaml_basic():
    yaml_data = """
input:
  id: 1
  name: beats
  plugin: beats
  bindPort: 3001
  bindAddress: 0.0.0.0
  flush_interval: 10
  flush_every: 15000
  next_error: "unknown"
  next: [2]

processor:
  id: 2
  plugin: loadJson
  next: ["agent"]
    """
    result = core.parser.yaml(yaml_data)[0]
    assert 1 in result
    assert result[1]["type"] == "input"
    assert result[1]["plugin"] == "beats"
    assert result[1]["enabled"] == True
    assert result[1]["properties"]["bindPort"] == 3001
    assert result[1]["properties"]["bindAddress"] == "0.0.0.0"
    assert result[1]["properties"]["next_error"] == "unknown"
    assert result[1]["next"] == [2]

    assert 2 in result
    assert result[2]["type"] == "processor"
    assert result[2]["plugin"] == "loadJson"
    assert result[2]["next"] == ["agent"]