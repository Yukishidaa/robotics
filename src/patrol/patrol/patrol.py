"""Publish a fixed velocity command from the latest turtlesim pose."""

from __future__ import annotations

from typing import Optional

from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
import math


def command_for_pose(pose: Optional[Pose], linear_speed: float, turn_rate: float) -> Twist:
    """Return the command for *pose*, or a safe stop before the first pose."""
    command = Twist()
    if pose is not None:
        command.linear.x = linear_speed
        command.angular.z = turn_rate
    return command


def validate_parameter(name: str, value: float) -> tuple[bool, str]:
    """Validate a parameter value. Returns (is_valid, error_message)."""
    if not math.isfinite(value):
        return False, f"{name} must be a finite number, got {value}"
    if name == "linear_speed":
        if value < 0.0 or value > 1.0:
            return False, f"linear_speed must be in [0, 1], got {value}"
    elif name == "turn_rate":
        if value < -1.0 or value > 1.0:
            return False, f"turn_rate must be in [-1, 1], got {value}"
    elif name == "publish_hz":
        if value < 1.0 or value > 30.0:
            return False, f"publish_hz must be in [1, 30], got {value}"
    return True, ""


class Patrol(Node):
    """Subscribe to the turtle pose and publish a periodic velocity command."""

    def __init__(self) -> None:
        super().__init__("patrol")
        self.last_pose: Optional[Pose] = None
        
        # Declare parameters with default values
        self.declare_parameter("linear_speed", 0.5)
        self.declare_parameter("turn_rate", 0.3)
        self.declare_parameter("publish_hz", 10.0)
        
        # Get initial parameter values
        self.linear_speed = self.get_parameter("linear_speed").get_parameter_value().double_value
        self.turn_rate = self.get_parameter("turn_rate").get_parameter_value().double_value
        self.publish_hz = self.get_parameter("publish_hz").get_parameter_value().double_value
        
        # Validate initial parameters
        for name, value in [("linear_speed", self.linear_speed), 
                             ("turn_rate", self.turn_rate), 
                             ("publish_hz", self.publish_hz)]:
            valid, error = validate_parameter(name, value)
            if not valid:
                self.get_logger().error(f"Invalid initial parameter: {error}")
                raise ValueError(error)
        
        self.pose_subscription = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.pose_callback,
            10,
        )
        self.command_publisher = self.create_publisher(Twist, "cmd_vel", 10)
        
        # Timer with initial period
        self.timer = self.create_timer(1.0 / self.publish_hz, self.timer_callback)
        
        # Parameter callback for dynamic reconfiguration
        self.add_on_set_parameters_callback(self.parameters_callback)

    def pose_callback(self, message: Pose) -> None:
        """Keep only the most recently received pose."""
        self.last_pose = message

    def timer_callback(self) -> None:
        """Publish a stop until a pose has arrived, then publish motion."""
        self.command_publisher.publish(command_for_pose(self.last_pose, self.linear_speed, self.turn_rate))

    def parameters_callback(self, parameters: list[Parameter]) -> SetParametersResult:
        """Handle dynamic parameter changes."""
        result = SetParametersResult(successful=True)
        timer_recreate = False
        new_publish_hz = self.publish_hz
        
        for param in parameters:
            if param.name == "linear_speed":
                valid, error = validate_parameter("linear_speed", param.value)
                if not valid:
                    result.successful = False
                    result.reason = error
                    return result
                self.linear_speed = param.value
                self.get_logger().info(f"linear_speed changed to {self.linear_speed}")
            elif param.name == "turn_rate":
                valid, error = validate_parameter("turn_rate", param.value)
                if not valid:
                    result.successful = False
                    result.reason = error
                    return result
                self.turn_rate = param.value
                self.get_logger().info(f"turn_rate changed to {self.turn_rate}")
            elif param.name == "publish_hz":
                valid, error = validate_parameter("publish_hz", param.value)
                if not valid:
                    result.successful = False
                    result.reason = error
                    return result
                new_publish_hz = param.value
                timer_recreate = True
        
        # Recreate timer if publish_hz changed
        if timer_recreate and new_publish_hz != self.publish_hz:
            self.timer.cancel()
            self.timer = self.create_timer(1.0 / new_publish_hz, self.timer_callback)
            self.publish_hz = new_publish_hz
            self.get_logger().info(f"publish_hz changed to {self.publish_hz}, timer recreated")
        
        return result


def main(args: Optional[list[str]] = None) -> None:
    """Run the patrol node until interrupted."""
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.command_publisher.publish(Twist())
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
