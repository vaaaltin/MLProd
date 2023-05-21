"""
docker build --tag my_zmq_worker .

docker run -d --network host my_zmq_worker

docker rm -f $(docker ps -a -q --filter "ancestor=my_zmq_worker")
"""

import subprocess


def run_cmd(cmd):
    """
    Runs any shell command.
    """

    return subprocess.run(
        ["/bin/sh", "-c", cmd],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode
