import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

class ScanFilter(Node):
    def __init__(self):
        super().__init__('scan_filter')
        self.sub = self.create_subscription(LaserScan, '/scan_raw', self.callback, 10)
        self.pub = self.create_publisher(LaserScan, '/scan', 10)
        
        self.angle_min = -1.92
        self.angle_max = 1.92
        self.get_logger().info(f'스캔 필터 시작: {math.degrees(self.angle_min):.0f}도 ~ {math.degrees(self.angle_max):.0f}도')

    def callback(self, msg):
        filtered = LaserScan()
        filtered.header = msg.header
        filtered.angle_min = self.angle_min
        filtered.angle_max = self.angle_max
        filtered.angle_increment = msg.angle_increment
        filtered.time_increment = msg.time_increment
        filtered.scan_time = msg.scan_time
        filtered.range_min = msg.range_min
        filtered.range_max = msg.range_max

        ranges = []
        intensities = []
        
        angle = msg.angle_min
        for i in range(len(msg.ranges)):
            if self.angle_min <= angle <= self.angle_max:
                ranges.append(msg.ranges[i])
                if msg.intensities:
                    intensities.append(msg.intensities[i])
            angle += msg.angle_increment

        filtered.ranges = ranges
        filtered.intensities = intensities
        self.pub.publish(filtered)

def main(args=None):
    rclpy.init(args=args)
    node = ScanFilter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
