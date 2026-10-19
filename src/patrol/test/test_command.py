"""Unit tests for command selection."""

import unittest
from geometry_msgs.msg import Twist

from patrol.patrol import command_for_pose


class TestCommandForPose(unittest.TestCase):
    def test_no_pose_produces_zero_command(self):
        command = command_for_pose(None)
        self.assertEqual(command.linear.x, 0.0)
        self.assertEqual(command.angular.z, 0.0)


    def test_pose_produces_expected_command(self):
        command = command_for_pose(object())
        self.assertEqual(command.linear.x, 0.5)
        self.assertEqual(command.angular.z, 0.3)
        self.assertEqual(command.linear.y, 0.0)
        self.assertEqual(command.angular.x, 0.0)
