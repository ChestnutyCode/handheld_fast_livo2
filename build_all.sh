#!/usr/bin/env bash

set -e

echo "=========================================="
echo " Handheld FAST-LIVO2 build"
echo "=========================================="

source /opt/ros/humble/setup.bash

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "[1/2] Building livox_ros_driver2..."

cd "$ROOT/ws_livox"

rm -rf build install log

colcon build \
  --symlink-install \
  --cmake-args \
  -DROS_EDITION=ROS2 \
  -DDISTRO_ROS=humble

source install/setup.bash

echo ""
echo "[2/2] Building FAST-LIVO2 workspace..."

cd "$ROOT/fast_ws"

rm -rf build install log

colcon build --symlink-install

echo ""
echo "=========================================="
echo " Build finished."
echo "=========================================="
