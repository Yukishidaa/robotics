"""Unit tests for command selection and parameter validation."""

import unittest
from geometry_msgs.msg import Twist

from patrol.patrol import command_for_pose, validate_parameter


class TestCommandForPose(unittest.TestCase):
    def test_no_pose_produces_zero_command(self):
        command = command_for_pose(None, 0.5, 0.3)
        self.assertEqual(command.linear.x, 0.0)
        self.assertEqual(command.angular.z, 0.0)

    def test_pose_produces_expected_command(self):
        command = command_for_pose(object(), 0.5, 0.3)
        self.assertEqual(command.linear.x, 0.5)
        self.assertEqual(command.angular.z, 0.3)
        self.assertEqual(command.linear.y, 0.0)
        self.assertEqual(command.angular.x, 0.0)

    def test_command_uses_given_parameters(self):
        command = command_for_pose(object(), 0.8, -0.2)
        self.assertEqual(command.linear.x, 0.8)
        self.assertEqual(command.angular.z, -0.2)


class TestValidateParameter(unittest.TestCase):
    def test_valid_linear_speed(self):
        valid, error = validate_parameter("linear_speed", 0.5)
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_linear_speed_at_bounds(self):
        valid, _ = validate_parameter("linear_speed", 0.0)
        self.assertTrue(valid)
        valid, _ = validate_parameter("linear_speed", 1.0)
        self.assertTrue(valid)

    def test_invalid_linear_speed_negative(self):
        valid, error = validate_parameter("linear_speed", -0.1)
        self.assertFalse(valid)
        self.assertIn("linear_speed", error)

    def test_invalid_linear_speed_above_one(self):
        valid, error = validate_parameter("linear_speed", 1.5)
        self.assertFalse(valid)
        self.assertIn("linear_speed", error)

    def test_valid_turn_rate(self):
        valid, error = validate_parameter("turn_rate", 0.3)
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_turn_rate_at_bounds(self):
        valid, _ = validate_parameter("turn_rate", -1.0)
        self.assertTrue(valid)
        valid, _ = validate_parameter("turn_rate", 1.0)
        self.assertTrue(valid)

    def test_invalid_turn_rate_below_minus_one(self):
        valid, error = validate_parameter("turn_rate", -1.5)
        self.assertFalse(valid)
        self.assertIn("turn_rate", error)

    def test_invalid_turn_rate_above_one(self):
        valid, error = validate_parameter("turn_rate", 1.5)
        self.assertFalse(valid)
        self.assertIn("turn_rate", error)

    def test_valid_publish_hz(self):
        valid, error = validate_parameter("publish_hz", 10.0)
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_publish_hz_at_bounds(self):
        valid, _ = validate_parameter("publish_hz", 1.0)
        self.assertTrue(valid)
        valid, _ = validate_parameter("publish_hz", 30.0)
        self.assertTrue(valid)

    def test_invalid_publish_hz_zero(self):
        valid, error = validate_parameter("publish_hz", 0.0)
        self.assertFalse(valid)
        self.assertIn("publish_hz", error)

    def test_invalid_publish_hz_negative(self):
        valid, error = validate_parameter("publish_hz", -5.0)
        self.assertFalse(valid)
        self.assertIn("publish_hz", error)

    def test_invalid_publish_hz_above_thirty(self):
        valid, error = validate_parameter("publish_hz", 35.0)
        self.assertFalse(valid)
        self.assertIn("publish_hz", error)

    def test_invalid_nan(self):
        valid, error = validate_parameter("linear_speed", float("nan"))
        self.assertFalse(valid)
        self.assertIn("finite", error)

    def test_invalid_inf(self):
        valid, error = validate_parameter("turn_rate", float("inf"))
        self.assertFalse(valid)
        self.assertIn("finite", error)
