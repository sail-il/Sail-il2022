#include "fusion.h"
#include "ros/ros.h"
#include <iostream>
#include <stdio.h>

#define PCL2_TOPIC "/zed2_left/zed_node_left/point_cloud/cloud_registered"
#define BB_TOPIC "/darknet_ros_left/bounding_boxes"

int main(int argc, char** argv){
  
  Fusion fusion;
  ros::init(argc, argv, "bb_pcl_fusion");

  ros::NodeHandle n;
  ros::Subscriber bb_sub = n.subscribe(BB_TOPIC,3,&Fusion::bb_callback,&fusion);
  ros::Subscriber pcl2_sub = n.subscribe(PCL2_TOPIC, 3 ,&Fusion::pcl2_callback, &fusion);
  ros::Publisher marker_pub = n.advertise<visualization_msgs::MarkerArray>("ball_marker",50);
  
  //create boundig box subsciber 
  ROS_INFO("starting node");
  
  // ros::spin();
  ros::Rate rate(30);
  while(ros::ok()){
    ros::spinOnce(); 
    ROS_INFO("spun once");
    marker_pub.publish(fusion.markerArray);
    rate.sleep(); 
  }

  return 0;
}