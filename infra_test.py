from unittest import TestCase
import pytest


@pytest.mark.usefixtures("host")
class TestRequirements(TestCase):

    def setUp(self):
        super(TestRequirements, self).setUp()

    def test_app_script(self):
        print("test_app_script")
        env_file = self.host.file('/www/hello.py')
        env_file.exists

    def test_app_html_template(self):
        print("test_app_html_template")
        env_file = self.host.file('/www/index.html')
        env_file.exists

    def test_process_running(self):
        print("test_process_running")
        processes = self.host.process.filter(user="root", comm="python")
        for p in processes:
            print(p.args)
        assert processes[0].args == 'python hello.py'
        assert len(processes) == 1

    def test_app_is_listening_in_port_80(self):
        print("test_app_is_listening_in_port_80")
        assert self.host.socket("tcp://0.0.0.0:80").is_listening
