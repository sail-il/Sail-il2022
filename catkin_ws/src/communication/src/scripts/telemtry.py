#!/usr/bin/env python2.7

import rospy
import rosbag
from datetime import datetime
#import std_msgs
#from visualization_msgs import MarkerArray
from sensor_msgs.msg import LaserScan, PointCloud2, Imu, Image

BUFFER_MAX = 10

LASERSCAN_TOPIC = "/laser/scan"
POINTCLOUD_TOPIC = "/quanergy/points"
CV_IMAGE_RAW_TOPIC = "/Zed2/zed_node/stereo_raw/image_raw"
CV_IMAGE_RECT_TOPIC = "/Zed2/zed_node/stereo_raw/image_rect"
CV_POINTCLOUD_TOPIC = "/Zed2/zed_node/point_cloud/cloud_registered"
IMU_TOPIC = "/imu/data"

class Laser:
    def __init__(self):
        self.bag    = rosbag.Bag('Laser' + datetime.now().strftime('%d_%m_%Y__%H_%M'), 'w')
        self.subscriber = rospy.Subscriber(CV_IMAGE_RECT_TOPIC, PointCloud2, self.PointCloudCallback)

    def PointCloudCallBack(self, msg):
        self.bag.write(POINTCLOUD_TOPIC, msg)
        rospy.loginfo("recived msg from POINTCLOUD_TOPIC!\n")

class cv:
    def __init__(self):
        self.bag = rosbag.Bag('cv' + datetime.now().strftime('%d_%m_%Y__%H_%M'), 'w')
        self.raw_subscribe = rospy.Subscriber(CV_IMAGE_RAW_TOPIC, Image, self.ImageRawCallback)
        self.rect_subsvribe = rospy.Subscriber(CV_IMAGE_RECT_TOPIC, Image, self.ImageRectCallback)
        self.pointcloud_subscribe = rospy.Subscriber(CV_IMAGE_RECT_TOPIC, PointCloud2, self.PointCloudCallback)
    
    def ImageRawCallBack(self, msg):
        self.bag.write(CV_IMAGE_RAW_TOPIC, msg)
        rospy.loginfo("CV raw image recived")
    
    def ImageRectCallBack(self,msg):
        self.bag.write(CV_IMAGE_RECT_TOPIC, msg)
        rospy.loginfo("CV rect image msg recived")

    def PointCloudCallBack(self, msg):
        self.bag.write(CV_POINTCLOUD_TOPIC, msg)
        rospy.loginfo("CV pointcloud msg recived")

class imu:
    def __init__(self):
        self.bag = rosbag.Bag('Imu' + datetime.now().strftime('%d_%m_%Y__%H_%M'), 'w')
        self.subscriber = rospy.Subscriber(IMU_TOPIC, Imu, self.ImuCallBack)

    def ImuCallBack(self, msg):
        self.bag.write(IMU_TOPIC, msg)
        rospy.loginfo("Imu data received!")


class subscribe_control:
    def __init__(self):
        self.cv_data = cv()
        self.Imu_data = imu()
        self.Laser_data = Laser()
    

if __name__ == '__main__':
    #new_bag = rospy.get_param("/start_new_bag")

    try:
        rospy.init_node('communication')
        main = subscribe_control()
        #if new_bag == True:
        #    data.Laser_data.bag.close()
        #    data.Laser_data.bag    = rosbag.Bag('Laser' + datetime.now().strftime('%d_%m_%Y__%H_%M'), 'w')
        #    new_bag = False
        rospy.spin()
    finally:   
        main.Laser_data.bag.close()
        main.Imu_data.bag.close()
        main.cv_data.bag.clode()