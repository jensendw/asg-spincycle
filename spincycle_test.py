import unittest
import mock
import os
from spincycle import *

def simple_urandom(length):
    return 'f' * length

def mock_get_autoscaling_group(asg_name):
    return {'AutoScalingGroups': []}

class TestRandom(unittest.TestCase):
    @mock.patch('os.urandom', side_effect=simple_urandom)
    def test_urandom(self, urandom_function):
        assert os.urandom(5) == 'fffff'

class TestSpincycle(unittest.TestCase):
    @mock.patch('get_autoscaling_group', side_effect=mock_get_autoscaling_group)
    def test_get_autoscaling_group(self, get_autoscaling_group):
        assert get_autoscaling_group('mooh') == {'AutoScalingGroups': []}

if __name__ == '__main__':
    unittest.main()
