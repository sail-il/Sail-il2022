#pragma once
#include <iostream>
#include <string>
#include <cmath>
#include <cfloat>
#include "ros/ros.h"
#include "sensor_msgs/PointCloud2.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "pcl/conversions.h"
#include "pcl_conversions/pcl_conversions.h"
#include "darknet_ros_msgs/BoundingBoxes.h"
#include "darknet_ros_msgs/BoundingBox.h"
#include "visualization_msgs/Marker.h"
#include "visualization_msgs/MarkerArray.h"
// #include "cv_lidar_fusion_pkg/relative_obstacle.h"
// #include "cv_lidar_fusion_pkg/relative_obstacles.h"

class Fusion{
  public:
    //cv_lidar_fusion_pkg::relative_obstaclesPtr rel_obst_arr;
    pcl::PointCloud<pcl::PointXYZ>::Ptr p_pcl;
    std::string func_param;
    //bounding boxes atribute
    visualization_msgs::MarkerArray markerArray;
    visualization_msgs::Marker::Ptr red_marker;
    visualization_msgs::Marker::Ptr green_marker;
  public:
    Fusion();

    void pcl2_callback(const sensor_msgs::PointCloud2ConstPtr& pcl2_msg);

    void bb_callback(const darknet_ros_msgs::BoundingBoxesPtr& bb_msg);

    //cv_lidar_fusion_pkg::relative_obstaclePtr

    // get_bb_pos(std::vector<darknet_ros_msgs::BoundingBox>::iterator bb);

    //void update_obst_arr(cv_lidar_fusion_pkg::relative_obstaclePtr);

    // void pub_rel_obst_arr();

    pcl::PointXYZ 
    get_point(std::vector<darknet_ros_msgs::BoundingBox>::iterator boundingbox,
    const pcl::PointCloud<pcl::PointXYZ>::Ptr p_pcl);

    // cv_lidar_fusion_pkg::relative_obstaclePtr 
    // point_from_subarray(pcl::PointCloud<pcl::PointXYZRGBA>::VectorType subarray,
    // std::string func_param);
};
