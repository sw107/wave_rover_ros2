import os
import xacro
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    nav2_params = os.path.join(
        get_package_share_directory('wave_rover_slam'),
        'config',
        'nav2_params.yaml'
    )

    map_yaml_file = LaunchConfiguration('map')

    declare_map_yaml_cmd = DeclareLaunchArgument(
        'map',
        default_value='',
        description='지도 yaml 파일 경로'
    )

    # xacro 파일을 urdf 문자열로 변환
    urdf_file = os.path.join(
    get_package_share_directory('wave_rover_slam'),
    'urdf',
    'wave_rover.urdf.xacro'
    )
    robot_description = xacro.process_file(urdf_file).toxml()

    return LaunchDescription([
        declare_map_yaml_cmd,

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

        # 지도 서버
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[
                nav2_params,
                {'yaml_filename': map_yaml_file}
            ],
            output='screen'
        ),

        # AMCL 노드
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            parameters=[nav2_params],
            output='screen'
        ),

        # Nav2 생명주기 관리자
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_localization',
            parameters=[{
                'use_sim_time': False,
                'autostart': True,
                'node_names': ['map_server', 'amcl']
            }],
            output='screen'
        ),

        # Nav2 컨트롤러 서버
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            parameters=[nav2_params],
            output='screen'
        ),

        # Nav2 플래너 서버
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            parameters=[nav2_params],
            output='screen'
        ),

        # Nav2 복구 서버
        Node(
            package='nav2_recoveries',
            executable='recoveries_server',
            name='recoveries_server',
            parameters=[nav2_params],
            output='screen'
        ),

        # Nav2 BT 네비게이터
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            parameters=[nav2_params],
            output='screen'
        ),

        # Nav2 생명주기 관리자 (네비게이션)
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            parameters=[{
                'use_sim_time': False,
                'autostart': True,
                'node_names': [
                    'controller_server',
                    'planner_server',
                    'recoveries_server',
                    'bt_navigator'
                ]
            }],
            output='screen'
        ),
    ])
