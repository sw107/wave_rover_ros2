from setuptools import find_packages, setup
package_name = 'wave_rover_bridge'
setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/wave_rover_bridge.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sw107',
    maintainer_email='sw107@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'wave_rover_bridge = wave_rover_bridge.wave_rover_bridge_node:main',
            'odom_publisher = wave_rover_bridge.odom_publisher:main'
        ],
    },
)
