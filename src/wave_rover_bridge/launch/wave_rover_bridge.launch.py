from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
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
