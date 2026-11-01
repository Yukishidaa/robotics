"""Launch robot_state_publisher with the Ackermann URDF model."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description() -> LaunchDescription:
    """Generate launch description for viewing the robot model."""
    
    pkg_share = get_package_share_directory('course_description')
    xacro_file = os.path.join(pkg_share, 'urdf', 'vehicle.urdf.xacro')
    
    # Аргумент для подключения к уже запущенному RViz или нет
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='false',
        description='Whether to launch RViz',
    )
    
    robot_description = Command(['xacro ', xacro_file])
    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )
    
    return LaunchDescription([
        use_rviz_arg,
        robot_state_publisher,
    ])
