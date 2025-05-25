import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(autouse=True)
def set_cwd(tmp_path, request):
    orig_cwd = os.getcwd()
    if orig_cwd == "/workspace":
        os.chdir("/workspace/accept")
    yield
    os.chdir(orig_cwd)

import core.globalSettings

class args:
    log_level = 10
    debug = False
    cache_dir = "cache"
    version = "1.3-pr"
    pipeline = "test_pipeline"
    config = "test_config.yaml"
    flush_timeout = 60
    flush_threads = 5
    flush_thread_max_memory = 1073741824
    component = "accept"
    main = True
    cache = "test"

core.globalSettings.args = args()