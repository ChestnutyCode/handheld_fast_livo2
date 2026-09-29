import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2

class CheckCloud(Node):
    def __init__(self):
        super().__init__('check_rgb_cloud')
        self.create_subscription(
            PointCloud2,
            '/cloud_registered',
            self.callback,
            10)

    def callback(self, msg):
        if msg.width == 0:
            return

        print("width =", msg.width)
        print("height =", msg.height)
        print("point_step =", msg.point_step)

        print("fields:")
        for f in msg.fields:
            print("  ", f.name, "offset =", f.offset,
                  "datatype =", f.datatype)

        rclpy.shutdown()

rclpy.init()
node = CheckCloud()
rclpy.spin(node)
