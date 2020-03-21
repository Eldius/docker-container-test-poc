import pytest
import subprocess
import os
import testinfra
import logging

DOCKER_IMAGE_NAME = 'eeacms/hello:latest'

logger = logging.getLogger('test_configuration')
logger.setLevel(logging.DEBUG)

# scope='session' uses the same container for all the tests;
# scope='function' uses a new container per test function.
@pytest.fixture(scope='class')
def host(request):
    # run a container
    print("Starting Docker container...")
    docker_id = subprocess.check_output(
        [
            'docker',
            'run',
            '-d',
            DOCKER_IMAGE_NAME,
        ]
    ).decode().strip()
    # return a testinfra connection to the container
    print(f"Docker ID: ${docker_id}")

    host = testinfra.get_host("docker://" + docker_id)
    request.cls.host = host
    yield host
    # at the end of the test suite, destroy the container

    print(f"Removing container: ${docker_id}")
    subprocess.check_call(['docker', 'rm', '-f', docker_id])
