"""Fixtures for the integration tests.

The integration tests treat the driver the way WeeWX does: they load it through
the public ``loader()`` entry point, drive it through ``genLoopPackets()``, and
replace the rtl_433 executable with a stand-in they control.
"""

import json
import sys

import pytest
import user.core as core

# ---------------------------------------------------------------------------
# a stand-in for the rtl_433 executable
# ---------------------------------------------------------------------------

# Behaviour is driven entirely by the FAKE_RTL433_SPEC environment variable,
# which the driver copies into the child environment.
FAKE_RTL433_SOURCE = """\
import json, os, sys, time

spec = json.loads(os.environ['FAKE_RTL433_SPEC'])

with open(spec['record'], 'w') as _f:
    json.dump({'argv': sys.argv, 'pid': os.getpid(), 'env': dict(os.environ)}, _f)
    _f.flush()

for line in spec['stdout']:
    sys.stdout.write(line + '\\n')
    sys.stdout.flush()

for line in spec['stderr']:
    sys.stderr.write(line + '\\n')
    sys.stderr.flush()

if spec['stay_alive']:
    while True:
        time.sleep(0.05)
"""


class FakeRTL433:
    """A fake rtl_433 executable and the command line that runs it."""

    def __init__(self, cmd, record):
        self.cmd = cmd
        self._record = record

    def record(self):
        """What the executable saw (argv, pid, env), or None before it starts."""
        try:
            return json.loads(self._record.read_text())
        except FileNotFoundError:
            return None


@pytest.fixture
def make_fake_rtl433(tmp_path, monkeypatch):
    """Build a fake rtl_433 that emits the requested output."""
    counter = iter(range(1000))

    def make(stdout=(), stderr=(), stay_alive=False):
        n = next(counter)
        script = tmp_path / ('fake_rtl433_%d.py' % n)
        record = tmp_path / ('fake_rtl433_%d.json' % n)
        script.write_text(FAKE_RTL433_SOURCE)
        monkeypatch.setenv(
            'FAKE_RTL433_SPEC',
            json.dumps(
                {
                    'stdout': list(stdout),
                    'stderr': list(stderr),
                    'stay_alive': stay_alive,
                    'record': str(record),
                }
            ),
        )
        return FakeRTL433('%s %s' % (sys.executable, script), record)

    return make


# ---------------------------------------------------------------------------
# a stand-in for the process manager
# ---------------------------------------------------------------------------


class _StubProcManager:
    """Feeds the driver canned rtl_433 output instead of running a process."""

    def __init__(self, state):
        self._state = state
        self._blocks = [list(block) for block in state['blocks']]

    def startup(self, cmd, path=None, ld_library_path=None):
        self._state['started'] = {'cmd': cmd, 'path': path, 'ld_library_path': ld_library_path}

    def running(self):
        return bool(self._blocks)

    def get_stdout(self):
        while self._blocks:
            yield self._blocks.pop(0)

    def get_stderr(self):
        return []

    def shutdown(self):
        self._state['shutdown'] = True


@pytest.fixture
def stub_rtl433(monkeypatch):
    """Replace the process manager; set ``state['blocks']`` before loading."""
    state = {'blocks': [], 'started': None, 'shutdown': False}
    monkeypatch.setattr(core, 'ProcManager', lambda: _StubProcManager(state))
    return state


# ---------------------------------------------------------------------------
# the driver, loaded the way WeeWX loads it
# ---------------------------------------------------------------------------


@pytest.fixture
def load_driver():
    """Load the driver through the module-level ``loader()``, as WeeWX does."""

    def load(**stanza):
        return core.loader({'SDR': stanza}, None)

    return load
