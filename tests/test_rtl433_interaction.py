"""How the driver drives the rtl_433 executable.

These use a fake rtl_433 (a small Python script) so we can check what the driver
does *to* the process: the command line it runs, the environment it passes, how
it reads the output, and how it shuts the process down.
"""

import itertools
import time

import pytest
import user.core as core

# Real rtl_433 text output.  rtl_433 in text mode emits one timestamped line per
# packet, which is what the process manager groups on.
TOWER_TEXT = (
    '2016-08-30 23:57:20 Acurite tower sensor 0x37FC Ch A: 26.7 C 80.1 F 16 % RH',
    '2016-08-30 23:57:21 Acurite tower sensor 0x37FC Ch A: 27.0 C 80.6 F 15 % RH',
)

TOWER_SENSOR_MAP = {
    'outTemp': 'temperature.*.AcuriteTowerPacket',
    'outHumidity': 'humidity.*.AcuriteTowerPacket',
}


def wait_until(predicate, timeout=5.0):
    """Poll until the predicate holds (or give up)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(0.02)
    return False


def collect_until(getter, timeout=5.0):
    """Repeatedly drain ``getter()`` until it yields something."""
    collected = []
    deadline = time.time() + timeout
    while time.time() < deadline:
        collected.extend(getter())
        if collected:
            break
        time.sleep(0.02)
    return collected


# --- what we run ------------------------------------------------------------


def test_it_runs_the_configured_command(make_fake_rtl433):
    fake = make_fake_rtl433()
    manager = core.ProcManager()
    try:
        manager.startup(fake.cmd + ' -M utc -F json')
        assert wait_until(lambda: fake.record() is not None)
        assert fake.record()['argv'][1:] == ['-M', 'utc', '-F', 'json']
    finally:
        manager.shutdown()


def test_it_passes_path_and_ld_library_path_to_the_process(make_fake_rtl433):
    fake = make_fake_rtl433()
    manager = core.ProcManager()
    try:
        manager.startup(fake.cmd, path='/opt/rtl-433/bin', ld_library_path='/opt/rtl-sdr/lib')
        assert wait_until(lambda: fake.record() is not None)

        env = fake.record()['env']
        assert env['PATH'].startswith('/opt/rtl-433/bin:')
        assert env['LD_LIBRARY_PATH'] == '/opt/rtl-sdr/lib'
    finally:
        manager.shutdown()


# --- what we do with its output ---------------------------------------------


def test_it_notices_when_the_process_is_gone(make_fake_rtl433):
    fake = make_fake_rtl433()  # exits immediately
    manager = core.ProcManager()
    manager.startup(fake.cmd)
    assert wait_until(lambda: not manager.running())
    manager.shutdown()


def test_stderr_from_rtl_433_is_surfaced(make_fake_rtl433):
    fake = make_fake_rtl433(stderr=['rtl_433: no tuner'], stay_alive=True)
    manager = core.ProcManager()
    try:
        manager.startup(fake.cmd)
        lines = collect_until(manager.get_stderr)
        assert any('no tuner' in line for line in lines)
    finally:
        manager.shutdown()


def test_a_packet_is_read_end_to_end_from_rtl_433(make_fake_rtl433):
    fake = make_fake_rtl433(stdout=TOWER_TEXT, stay_alive=True)
    driver = core.loader({'SDR': {'cmd': fake.cmd, 'sensor_map': TOWER_SENSOR_MAP}}, None)
    try:
        packets = list(itertools.islice(driver.genLoopPackets(), 1))
    finally:
        driver.closePort()

    assert packets[0]['outTemp'] == pytest.approx(26.7)
    assert packets[0]['outHumidity'] == pytest.approx(16.0)


# --- what we do to it on the way out ----------------------------------------


def test_closePort_terminates_rtl_433(make_fake_rtl433):
    fake = make_fake_rtl433(stay_alive=True)
    driver = core.loader({'SDR': {'cmd': fake.cmd, 'sensor_map': TOWER_SENSOR_MAP}}, None)

    process = driver._mgr._process
    assert process.poll() is None  # running

    driver.closePort()

    assert process.poll() is not None  # killed
