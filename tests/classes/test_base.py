import pytest
import time

import classes.base
import core.globalSettings

def test_base():
    base = classes.base.base()
    assert base.nextBehavior == 0
    assert hasattr(base, '_processStats')
    assert isinstance(base._processStats, dict)
    assert 'time' in base._processStats
    assert 'events' in base._processStats
    assert isinstance(base._processStats['time'], dict)
    assert "total" in base._processStats['time']
    assert base._processStats['time']['total'] == 0
    assert base._processStats['time']['last'] == 0
    assert base._processStats['time']['first'] == 0
    assert isinstance(base._processStats['events'], dict)
    assert base._processStats['events']['count'] == 0

def test_processStats():
    base = classes.base.base()
    base.id = "test_id"
    stats = base.processStats()
    assert stats["cache"] == core.globalSettings.args.cache
    assert stats["id"] == "test_id"
    assert stats["events"]["count"] == 0
    assert isinstance(stats, dict)

def test_updateProcessStats():
    base = classes.base.base()
    base.id = "test_id"
    eventStartTime = time.perf_counter_ns()
    base.updateProcessStats(eventStartTime)
    
    assert base._processStats["time"]["total"] > 0
    assert base._processStats["time"]["last"] > 0
    assert base._processStats["time"]["first"] > 0
    assert base._processStats["events"]["count"] == 1

    stats = base.processStats()
    assert stats["time"]["total"] == base._processStats["time"]["total"]
    assert stats["time"]["last"] == base._processStats["time"]["last"]
    assert stats["time"]["first"] == base._processStats["time"]["first"]
    assert stats["events"]["count"] == base._processStats["events"]["count"]
    assert "average" in stats["time"]
    assert isinstance(stats["time"]["average"], dict)
    assert "1" in stats["time"]["average"]
    assert "100" in stats["time"]["average"]
    assert "1000" in stats["time"]["average"]
    assert stats["time"]["average"]["1"] > 0
    assert stats["time"]["average"]["100"] > 0
    assert stats["time"]["average"]["1000"] > 0
    assert stats["time"]["average"]["1"] == stats["time"]["total"] / stats["events"]["count"]
    assert stats["time"]["average"]["100"] == (stats["time"]["total"] / stats["events"]["count"]) * 100
    assert stats["time"]["average"]["1000"] == (stats["time"]["total"] / stats["events"]["count"]) * 1000