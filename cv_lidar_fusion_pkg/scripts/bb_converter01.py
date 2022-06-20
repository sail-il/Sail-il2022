#!/usr/bin/env python3
import rospy
from darknet_ros_msgs.msg import BoundingBox, BoundingBoxes
from cv_lidar_fusion_pkg.msg import relative_obstacle, relative_obstacles
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import numpy as np

cloud_projection = 0
global_var = 0

def bb_to_relative(bb):
    print(len(cloud_proj))
    lidar_sub()
    rel_obst = relative_obstacle()
    rel_obst.id = bb.id
    rel_obst.Class = bb.Class
    rel_obst.probability = bb.probability
    lower_left_cloud = bb.xmin*cloud.point_step + bb.ymin*cloud.row_step
    bb_width_cloud = (bb.xmax - bb.xmin)*cloud.point_step
    bb_height_cloud = bb.ymax - bb.ymin
    temp_array=[]
    for row in range(bb_height_cloud):
        row_start = lower_left_cloud + bb_width_cloud*row
        temp_array.append(cloud_proj[row_start:row_start+bb_width_cloud])
    bb_array = np.array(temp_array)
    print(bb_array)

def converter(msg,args):
    print(args[0])
    rospy.loginfo("message recived from darknet")
    rospy.loginfo(cloud.header)
    for bb in msg.bounding_boxes:
        rospy.loginfo(bb)
        rel_obst = bb_to_relative(bb)

def cloud_update(msg,args):
    print("cloud_update")
    cloud.header = msg.header
    cloud.height = msg.height
    cloud.width = msg.width
    cloud.data = msg.data
    cloud.is_bigendian = msg.is_bigendian
    cloud.is_dense = msg.is_dense
    cloud.point_step = msg.point_step
    cloud.row_step = msg.row_step
    # args[0] = pc2.read_points_list(msg,field_names=("x","y","z","rgb"),skip_nans=True)
    global_var = global_var + 1
    print(global_var)

    
def bb_sub():
    rate = rospy.Rate(10)
    rospy.loginfo("listening for bounding boxes from darknet")
    bound_box_sub = rospy.Subscriber("/darknet_ros/bounding_boxes",BoundingBoxes,callback=converter,callback_args=[cloud_projection])
    

def lidar_sub():
    rate = rospy.Rate(5)
    rospy.loginfo("listening for pointcloud")
    lidar_sub = rospy.Subscriber("/zed2/zed_node/point_cloud/cloud_registered",PointCloud2,callback=cloud_update,callback_args=[cloud_projection])
    

def obstacle_publisher():
    rate = rospy.Rate(5)
    rospy.loginfo("publishing relative obsticales")
    obstacle = relative_obstacles()
    relative_obstacles.obstacle_array = []
    obst_pub = rospy.Publisher("/fusion/relative_obstacles",relative_obstacles,queue_size=10)
    while not rospy.is_shutdown():
        print(cloud_projection)
        obst_pub.publish(obstacle)
        rate.sleep()


if __name__ == '__main__':
    rospy.init_node("bb_converter",anonymous=True)
    rospy.loginfo("bb_converter startred")
    obstacles_msg = relative_obstacles()
    obstacles_msg.obstacle_array = []
    cloud = PointCloud2()
    cloud_proj = []
 
    # bb_sub(cloud_proj)
    lidar_sub()
    obstacle_publisher()
    
    

  