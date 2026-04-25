import rclpy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

msg = """
Reading from the keyboard and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%
anything else : stop

CTRL-C to quit
"""

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = rclpy.create_node('teleop_twist_keyboard')
    pub = node.create_publisher(Twist, 'cmd_vel', 10)

    speed = 0.5
    turn = 1.0
    try:
        print(msg)
        while True:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
            else:
                key = ''
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

            x = 0.0; th = 0.0
            if key == 'i': x = 1.0
            elif key == 'k': x = 0.0; th = 0.0
            elif key == 'j': th = 1.0
            elif key == 'l': th = -1.0
            elif key == 'u': x = 1.0; th = 1.0
            elif key == 'o': x = 1.0; th = -1.0
            elif key == 'm': x = -1.0; th = -1.0
            elif key == ',' : x = -1.0
            elif key == '.' : x = -1.0; th = 1.0
            elif key == '\x03': break

            twist = Twist()
            twist.linear.x = x * speed
            twist.angular.z = th * turn
            pub.publish(twist)
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        rclpy.shutdown()

if __name__ == '__main__':
    main()
