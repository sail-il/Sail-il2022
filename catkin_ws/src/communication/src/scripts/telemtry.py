#!/usr/bin/env python2.7

import rospy
import rosbag
from datetime import datetime
#import std_msgs
from visualization_msgs.msg import MarkerArray
from sensor_msgs.msg import LaserScan, PointCloud2, Imu, Image
from ublox_msgs.msg import NavSAT

BUFFER_MAX = 10

LASERSCAN_TOPIC = "/laser/scan"
POINTCLOUD_TOPIC = "/quanergy/points"
CV_IMAGE_RAW_TOPIC = "/zed2_left/zed_node_left/stereo_raw/image_raw_color"
CV_IMAGE_RECT_TOPIC = "/zed2_left/zed_node_left/stereo_raw/image_rect"
CV_POINTCLOUD_TOPIC = "/zed2_left/zed_node_left/point_cloud/cloud_registered"
BALL_MARKER_TOPIC= "/ball_marker"
IMU_TOPIC = "/imu/data"
GPS_TOPIC = "/ublox/fix"
#LOG_DIR = "~/Sail-il2022/catkin_ws/src/communication/logs/"
LOG_DIR = ""

class Laser:
    def __init__(self):
        self.bag    = rosbag.Bag(LOG_DIR + 'Laser' + datetime.now().strftime('%d_%m_%Y__%H_%M')+".bag", 'w')
        self.subscriber = rospy.Subscriber(CV_IMAGE_RECT_TOPIC, PointCloud2, self.PointCloudCallBack)

    def PointCloudCallBack(self, msg):
        self.bag.write(POINTCLOUD_TOPIC, msg)
        rospy.loginfo("recived msg from POINTCLOUD_TOPIC!\n")

class cv:
    def __init__(self):
        self.bag = rosbag.Bag(LOG_DIR+'cv_' + datetime.now().strftime('%d_%m_%Y__%H_%M') +".bag" , 'w')
        #self.raw_subscribe = rospy.Subscriber(CV_IMAGE_RAW_TOPIC, Image, self.ImageRawCallBack)
        #self.rect_subscribe = rospy.Subscriber(CV_IMAGE_RECT_TOPIC, Image, self.ImageRectCallBack)
        #self.pointcloud_subscribe = rospy.Subscriber(CV_POINTCLOUD_TOPIC, PointCloud2, self.PointCloudCallBack)
        self.ballmarker_subscribe = rospy.Subscriber(BALL_MARKER_TOPIC, MarkerArray, self.BallMarkerCallBack)

    def ImageRawCallBack(self, msg):
        self.bag.write(CV_IMAGE_RAW_TOPIC, msg)
        data = msg.data
        rospy.loginfo("image width=%d, image height=%d",msg.width,msg.height)
        rospy.loginfo("CV raw image recived")
    
    def ImageRectCallBack(self,msg):
        self.bag.write(CV_IMAGE_RECT_TOPIC, msg)
        rospy.loginfo("CV rect image msg recived")

    def PointCloudCallBack(self, msg):
        self.bag.write(CV_POINTCLOUD_TOPIC, msg)
        rospy.loginfo("CV pointcloud msg recived")
    
    def BallMarkerCallBack(self,msg):
        self.bag.write(BALL_MARKER_TOPIC, msg)
        rospy.loginfo("CV ball marker msg recived")

class imu:
    def __init__(self):
        self.bag = rosbag.Bag(LOG_DIR +'Imu' + datetime.now().strftime('%d_%m_%Y__%H_%M')+".bag", 'w')
        self.subscriber = rospy.Subscriber(IMU_TOPIC, Imu, self.ImuCallBack)

    def ImuCallBack(self, msg):
        self.bag.write(IMU_TOPIC, msg)
        rospy.loginfo("Imu data received!")

class gps:
    def __init__(self):
        self.bag = rosbag.Bag(LOG_DIR +'GPS' + datetime.now().strftime('%d_%m_%Y__%H_%M')+".bag", 'w')
        self.subscriber = rospy.Subscriber(GPS_TOPIC, NavSAT, self.GPSCallBack)

    def GPSCallBack(self, msg):
        self.bag.write(GPS_TOPIC, msg)
        rospy.loginfo("GPS data received!")

class subscribe_control:
    def __init__(self):
        self.cv_data = cv()
        self.Imu_data = imu()
        self.Laser_data = Laser()
        self.gps_data = gps()
    

if __name__ == '__main__':
    #new_bag = rospy.get_param("/start_new_bag")
    rospy.init_node('communication')
    main = subscribe_control()
    try:
        #if new_bag == True:
        #    data.Laser_data.bag.close()
        #    data.Laser_data.bag    = rosbag.Bag('Laser' + datetime.now().strftime('%d_%m_%Y__%H_%M'), 'w')
        #    new_bag = False
        rospy.spin()
    finally:   
        main.Laser_data.bag.close()
        main.Imu_data.bag.close()
        main.cv_data.bag.close()
        main.gps_data.bag.close()