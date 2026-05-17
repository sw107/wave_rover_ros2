import rclpy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty

msg = """
WAVE ROVER 키보드 조종
---------------------------
이동:
   u    i    o
   j    k    l
   m    ,    .

q/z : 전체 속도 10% 증가/감소
w/x : 직선 속도만  10% 증가/감소
e/c : 회전 속도만  10% 증가/감소
space / k : 정지
CTRL-C    : 종료
"""

moveBindings = {
    'i': (1.0,  0.0),
    'u': (1.0,  1.0),
    'o': (1.0, -1.0),
    'j': (0.0,  1.0),
    'l': (0.0, -1.0),
    'm': (-1.0, 1.0),
    ',': (-1.0,  0.0),
    '.': (-1.0, -1.0),
}

speedBindings = {
    'q': (1.1, 1.1),
    'z': (0.9, 0.9),
    'w': (1.1, 1.0),
    'x': (0.9, 1.0),
    'e': (1.0, 1.1),
    'c': (1.0, 0.9),
}


def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1) if rlist else ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def printSpeed(speed, turn):
    print(f'\r직선 속도: {speed:.3f} m/s  회전 속도: {turn:.3f} rad/s    ', end='')


def main():
    settings = termios.tcgetattr(sys.stdin)

    rclpy.init()
    node = rclpy.create_node('teleop_twist_keyboard')
    pub = node.create_publisher(Twist, 'cmd_vel', 10)

    speed = 0.3   # m/s  (nav2_params.yaml 최대값과 동일)
    turn = 1.0    # rad/s
    x = 0.0
    th = 0.0

    try:
        print(msg)
        printSpeed(speed, turn)

        while True:
            key = getKey(settings)

            if key in moveBindings:
                x, th = moveBindings[key]
            elif key in speedBindings:
                sp_mult, tu_mult = speedBindings[key]
                speed = speed * sp_mult
                turn = turn * tu_mult
                x = 0.0
                th = 0.0
                printSpeed(speed, turn)
            elif key in (' ', 'k'):
                x = 0.0
                th = 0.0
            elif key == '\x03':   # CTRL-C
                break
            else:
                # 인식 못한 키 or 타임아웃(key=='') → 정지
                x = 0.0
                th = 0.0

            twist = Twist()
            twist.linear.x = x * speed
            twist.angular.z = th * turn
            pub.publish(twist)
            rclpy.spin_once(node, timeout_sec=0.0)

    except Exception as e:
        print(e)
    finally:
        # 종료 시 정지 명령 전송
        twist = Twist()
        pub.publish(twist)
        rclpy.spin_once(node, timeout_sec=0.1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        rclpy.shutdown()


if __name__ == '__main__':
    main()
