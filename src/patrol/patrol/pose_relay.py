"""Pose relay node: reads /turtle1/pose and publishes sensor_pose with best_effort QoS."""

from __future__ import annotations

from typing import Optional

from turtlesim_msgs.msg import Pose
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy


class PoseRelay(Node):
    """Subscribe to /turtle1/pose and republish as sensor_pose with best_effort."""

    def __init__(self) -> None:
        super().__init__("pose_relay")
        
        # Best effort QoS profile for sensor data
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        
        self.pose_subscription = self.create_subscription(
            Pose,
            "/turtle1/pose",
            self.pose_callback,
            qos_profile,
        )
        self.pose_publisher = self.create_publisher(
            Pose,
            "sensor_pose",
            qos_profile,
        )

    def pose_callback(self, message: Pose) -> None:
        """Republish the received pose."""
        self.pose_publisher.publish(message)


def main(args: Optional[list[str]] = None) -> None:
    """Run the pose relay node until interrupted."""
    rclpy.init(args=args)
    node = PoseRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
