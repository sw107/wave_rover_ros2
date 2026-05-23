import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import json

class WaveRoverBridge(Node):
    def __init__(self):
        super().__init__('wave_rover_bridge')
        
        # 파라미터 선언
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        
        port = self.get_parameter('port').value
        baudrate = self.get_parameter('baudrate').value
        
        # 시리얼 연결
        try:
            self.serial = serial.Serial(port, baudrate, timeout=1)
            self.get_logger().info(f'WAVE ROVER 연결 성공: {port}')
        except Exception as e:
            self.get_logger().error(f'시리얼 연결 실패: {e}')
            self.serial = None
        
        # /cmd_vel 구독
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        # 하트비트 타이머 (3초마다 정지 명령 방지)
        self.timer = self.create_timer(1.0, self.heartbeat)
        self.last_cmd = {'T': 1, 'L': 0, 'R': 0}

    def cmd_vel_callback(self, msg):
        linear = msg.linear.x   # 전진/후진
        angular = msg.angular.z  # 좌/우 회전
        
        # 차동 구동 변환
        TURNGAIN = 2.0 
        left = linear - angular * TURNGAIN
        right = linear + angular * TURNGAIN
        
        # -1.0 ~ 1.0 범위로 클램핑
        left = max(-1.0, min(1.0, left))
        right = max(-1.0, min(1.0, right))
        
        self.last_cmd = {'T': 1, 'L': round(left, 2), 'R': round(right, 2)}
        self.send_command(self.last_cmd)

    def heartbeat(self):
        self.send_command(self.last_cmd)

    def send_command(self, cmd):
        if self.serial and self.serial.is_open:
            try:
                msg = json.dumps(cmd) + '\n'
                self.serial.write(msg.encode())
            except Exception as e:
                self.get_logger().error(f'전송 실패: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = WaveRoverBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
