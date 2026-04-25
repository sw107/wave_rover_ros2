import os
from ament_index_python.packages import get_package_share_directory
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory('wave_rover_slam'),
        'urdf',
        'wave_rover.urdf.xacro'
    )
    robot_description = xacro.process_file(urdf_file).toxml()
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),
        Node(
            package='wave_rover_bridge',
            executable='odom_publisher',
            name='odom_publisher',
            output='screen'
        ),
        Node(
            package='wave_rover_bridge',
            executable='wave_rover_bridge_node',
            name='wave_rover_bridge',
            parameters=[
                {'port': '/dev/ttyUSB0'},
                {'baudrate': 115200}
            ],
            output='screen'
        )
    ])
