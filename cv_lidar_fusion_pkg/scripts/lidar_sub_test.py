#!/usr/bin/env python3
import rospy
from cv_lidar_fusion_pkg.msg import relative_obstacle, relative_obstacles
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import numpy as np




def converter(cloud_proj):
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    for point in cloud_proj[10:20]:
      rospy.loginfo(point)
    rate.sleep()


def cloud_update(msg,args):
    args[0].header = msg.header
    args[0].height = msg.height
    args[0].width = msg.width
    args[0].data = msg.data
    args[0].is_bigendian = msg.is_bigendian
    args[0].is_dense = msg.is_dense
    args[0].point_step = msg.point_step
    args[0].row_step = msg.row_step
    args[1] = pc2.read_points_list(msg,field_names=("x","y","z","rgb"),skip_nans=True)


def lidar_sub(cloud_obj,cloud_proj):
    rate = rospy.Rate(20)
    rospy.loginfo("listening for pointcloud")
    rospy.Subscriber("/zed2/zed_node/point_cloud/cloud_registered",PointCloud2,callback=cloud_update,callback_args=[cloud_obj, cloud_proj])
    rate.sleep()


if __name__ == '__main__':
    rospy.init_node("lidar_sub_test",anonymous=True)
    rospy.loginfo("lidar_sub_test startred")
    cloud = PointCloud2()
    cloud_projection = []
    lidar_sub(cloud, cloud_projection)
    converter(cloud_projection)
    rospy.spin()

  