"""Launch file for patrol system with namespace, recording, and QoS configuration."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    """Generate the launch description for patrol system."""
    
    # Declare launch arguments
    namespace_arg = DeclareLaunchArgument(
        "namespace",
        default_value="robot_a",
        description="Namespace for the robot (e.g., robot_a, robot_b)",
    )
    
    record_arg = DeclareLaunchArgument(
        "record",
        default_value="false",
        description="Whether to record sensor_pose topic to MCAP bag",
    )
    
    bag_dir_arg = DeclareLaunchArgument(
        "bag_dir",
        default_value="evidence/pr05/bag",
        description="Directory to save the MCAP bag",
    )
    
    subscriber_reliability_arg = DeclareLaunchArgument(
        "subscriber_reliability",
        default_value="best_effort",
        description="Reliability QoS for the subscriber: reliable or best_effort",
    )
    
    # Namespace configuration
    namespace = LaunchConfiguration("namespace")
    record = LaunchConfiguration("record")
    bag_dir = LaunchConfiguration("bag_dir")
    subscriber_reliability = LaunchConfiguration("subscriber_reliability")
    
    # Turtlesim node (global, not namespaced)
    turtlesim_node = Node(
        package="turtlesim",
        executable="turtlesim_node",
        name="turtlesim_node",
        output="screen",
    )
    
    # Patrol node in namespace
    patrol_node = Node(
        package="patrol",
        executable="patrol",
        name="patrol",
        namespace=namespace,
        output="screen",
        remappings=[
            ("cmd_vel", "/turtle1/cmd_vel"),
        ],
        parameters=[
            {"linear_speed": 0.5},
            {"turn_rate": 0.3},
            {"publish_hz": 10.0},
        ],
    )
    
    # Pose relay node in namespace
    pose_relay_node = Node(
        package="patrol",
        executable="pose_relay",
        name="pose_relay",
        namespace=namespace,
        output="screen",
    )
    
    # QoS subscriber node in namespace
    qos_subscriber_node = Node(
        package="patrol",
        executable="qos_subscriber",
        name="qos_subscriber",
        namespace=namespace,
        output="screen",
        parameters=[
            {"reliability": subscriber_reliability},
        ],
    )
    
    # Rosbag recorder (conditional) - use shell to resolve namespace
    recorder = ExecuteProcess(
        condition=IfCondition(record),
        cmd=[
            "bash", "-c",
            ["ros2 bag record -s mcap -o ", bag_dir, " --topics ", namespace, "/sensor_pose"],
        ],
        output="screen",
    )
    
    return LaunchDescription([
        namespace_arg,
        record_arg,
        bag_dir_arg,
        subscriber_reliability_arg,
        turtlesim_node,
        patrol_node,
        pose_relay_node,
        qos_subscriber_node,
        recorder,
    ])
