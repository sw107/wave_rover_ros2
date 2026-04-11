#!/bin/bash
echo "=== ROS2 Foxy 자동 설치 스크립트 ==="

# 1. 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 2. locale 설정
sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# 3. ROS2 저장소 추가
sudo apt install -y software-properties-common curl apt-transport-https ca-certificates
sudo add-apt-repository universe -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | gpg --dearmor | sudo tee /usr/share/keyrings/ros-archive-keyring.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 4. ROS2 설치
sudo apt update
sudo apt install -y ros-foxy-ros-base

# 5. 필수 패키지 설치
sudo apt install -y python3-colcon-common-extensions python3-rosdep python3-argcomplete
sudo apt install -y ros-foxy-slam-toolbox ros-foxy-nav2-bringup ros-foxy-navigation2
sudo apt install -y ros-foxy-rplidar-ros

# 6. rosdep 초기화
sudo rosdep init
rosdep update

# 7. 환경 설정
echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
echo "source ~/wave_rover_ros2/install/setup.bash" >> ~/.bashrc

# 8. 빌드
cd ~/wave_rover_ros2
colcon build

# 9. pyserial 설치
pip install pyserial

echo "=== 설치 완료! ==="
echo "이제 GitHub에서 코드를 clone 하세요."
echo "cd ~/ros2_ws/src && git clone https://github.com/sw107/wave_rover_ros2.git"
