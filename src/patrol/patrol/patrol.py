"""Publish a fixed velocity command from the latest turtlesim pose."""

from __future__ import annotations

from typing import Optional

from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose

import rclpy
from rclpy.node import Node


def command_for_pose(pose: Optional[Pose]) -> Twist:
    """Return the command for *pose*, or a safe stop before the first pose."""
    command = Twist()
    if pose is not None:
        command.linear.x = 0.5
        command.angular.z = 0.3
    return command


class Patrol(Node):
    """Subscribe to the turtle pose and publish a periodic velocity command."""

    def __init__(self) -> None:
        super().__init__("patrol")
        self.last_pose: Optional[Pose] = None
        self.pose_subscription = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.pose_callback,
            10,
        )
        self.command_publisher = self.create_publisher(Twist, "cmd_vel", 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def pose_callback(self, message: Pose) -> None:
        """Keep only the most recently received pose."""
        self.last_pose = message

    def timer_callback(self) -> None:
        """Publish a stop until a pose has arrived, then publish motion."""
        self.command_publisher.publish(command_for_pose(self.last_pose))


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
