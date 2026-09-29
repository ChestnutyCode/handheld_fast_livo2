#!/usr/bin/env python3

import time
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import Image
from livox_ros_driver2.msg import CustomMsg


def stamp_to_ns(stamp):
    return stamp.sec * 1_000_000_000 + stamp.nanosec


class SyncCheck(Node):

    def __init__(self):
        super().__init__('sync_check')

        # 保存最近几十帧雷达
        self.lidar_stamps = deque(maxlen=50)

        self.create_subscription(
            CustomMsg,
            '/livox/lidar',
            self.lidar_callback,
            qos_profile_sensor_data
        )

        self.create_subscription(
            Image,
            '/left_camera/image',
            self.image_callback,
            qos_profile_sensor_data
        )

        print('等待 LiDAR 和 Camera 数据...')

    def lidar_callback(self, msg):
        t = stamp_to_ns(msg.header.stamp)
        self.lidar_stamps.append(t)

    def image_callback(self, msg):
        if not self.lidar_stamps:
            return

        image_t = stamp_to_ns(msg.header.stamp)

        # 在最近的雷达时间戳中寻找与图像最接近的一帧
        lidar_t = min(
            self.lidar_stamps,
            key=lambda x: abs(x - image_t)
        )

        diff_ms = (image_t - lidar_t) / 1e6

        print(
            f'Camera: {image_t / 1e9:.9f}   '
            f'LiDAR: {lidar_t / 1e9:.9f}   '
            f'dt: {diff_ms:+.3f} ms'
        )


def main():
    rclpy.init()
    node = SyncCheck()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


