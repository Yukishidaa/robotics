"""QoS subscriber node: subscribes to sensor_pose with configurable reliability."""

from __future__ import annotations

from typing import Optional

from turtlesim_msgs.msg import Pose
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult


class QoSSubscriber(Node):
    """Subscribe to sensor_pose with configurable reliability QoS."""

    def __init__(self) -> None:
        super().__init__("qos_subscriber")
        
        self.declare_parameter("reliability", "reliable")
        reliability_str = self.get_parameter("reliability").get_parameter_value().string_value
        
        reliability = ReliabilityPolicy.RELIABLE if reliability_str == "reliable" else ReliabilityPolicy.BEST_EFFORT
        
        qos_profile = QoSProfile(
            reliability=reliability,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        
        self.subscription = self.create_subscription(
            Pose,
            "sensor_pose",
            self.callback,
            qos_profile,
        )
        self.get_logger().info(f"Subscribing to sensor_pose with {reliability_str} reliability")

    def callback(self, message: Pose) -> None:
        """Log received message."""
        self.get_logger().info(f"Received: x={message.x:.2f}, y={message.y:.2f}, theta={message.theta:.2f}")


def main(args: Optional[list[str]] = None) -> None:
    """Run the QoS subscriber node until interrupted."""
    rclpy.init(args=args)
    node = QoSSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
