#!/usr/bin/env python3
"""A stand-in for the rtl_433 executable, used by the integration tests.

Behaviour is driven entirely by the ``FAKE_RTL433_SPEC`` environment variable (a
JSON object), which the driver copies into the child environment:

    stdout      list of lines to write to stdout
    stderr      list of lines to write to stderr
    stay_alive  if true, keep running until the driver kills us
    record      path to write what we saw (argv, pid, env) to
"""

import json
import os
import sys
import time


def main():
    spec = json.loads(os.environ['FAKE_RTL433_SPEC'])

    with open(spec['record'], 'w') as f:
        json.dump({'argv': sys.argv, 'pid': os.getpid(), 'env': dict(os.environ)}, f)
        f.flush()

    for line in spec['stdout']:
        sys.stdout.write(line + '\n')
        sys.stdout.flush()

    for line in spec['stderr']:
        sys.stderr.write(line + '\n')
        sys.stderr.flush()

    if spec['stay_alive']:
        while True:
            time.sleep(0.05)


if __name__ == '__main__':
    main()
