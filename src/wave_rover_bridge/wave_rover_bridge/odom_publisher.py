import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, TransformStamped
from tf2_ros import TransformBroadcaster
import math

class OdomPublisher(Node):
    def __init__(self):
        super().__init__('odom_publisher')

        # 로봇 위치 초기값
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # 이전 시간
        self.last_time = self.get_clock().now()

        # /cmd_vel 구독 (브리지 노드가 ESP32로 보내는 속도 명령을 그대로 사용)
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # /odom 퍼블리셔
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)

        # TF 브로드캐스터 (odom → base_footprint 변환 퍼블리시)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.linear_x = 0.0
        self.angular_z = 0.0

        # 10Hz로 오도메트리 업데이트
        self.timer = self.create_timer(0.1, self.update_odom)

        self.get_logger().info('오도메트리 노드 시작')

    def cmd_vel_callback(self, msg):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z

    def update_odom(self):
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time

        # Dead Reckoning 위치 계산
        delta_x = self.linear_x * math.cos(self.theta) * dt
        delta_y = self.linear_x * math.sin(self.theta) * dt
        delta_theta = self.angular_z * dt

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta

        # 쿼터니언 변환 (yaw만 사용)
        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        # TF 퍼블리시 (odom → base_footprint)
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_footprint'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw
        self.tf_broadcaster.sendTransform(t)

        # /odom 토픽 퍼블리시
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_footprint'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = 0.0
        odom.pose.pose.orientation.y = 0.0
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.twist.twist.linear.x = self.linear_x
        odom.twist.twist.angular.z = self.angular_z

        self.odom_pub.publish(odom)

def main(args=None):
    rclpy.init(args=args)
    node = OdomPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
