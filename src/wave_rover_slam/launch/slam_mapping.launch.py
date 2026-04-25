import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    slam_params = os.path.join(
        get_package_share_directory('wave_rover_slam'),
        'config',
        'slam_toolbox_params.yaml'
    )

    urdf_file = os.path.join(
        get_package_share_directory('wave_rover_slam'),
        'urdf',
        'wave_rover.urdf.xacro'
    )
    robot_description = xacro.process_file(urdf_file).toxml()

    return LaunchDescription([

        # robot_state_publisher 노드
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),

        # RPLIDAR 노드
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='rplidar',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'serial_baudrate': 115200,
                'frame_id': 'laser',
                'angle_compensate': True,
                'scan_mode': 'Standard',
            }],
            output='screen'
        ),

        # WAVE ROVER 브리지 노드
        Node(
            package='wave_rover_bridge',
            executable='wave_rover_bridge',
            name='wave_rover_bridge',
            output='screen'
        ),

        # SLAM Toolbox 노드 (온라인 비동기 모드)
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            parameters=[slam_params],
            output='screen'
        ),
    ])
