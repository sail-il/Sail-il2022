#include "fusion.h"
#include <typeinfo>
//declerations
bool check_nan_inf(pcl::PointXYZ point);
pcl::PointXYZ avg_point(std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>> subarray);
visualization_msgs::Marker create_marker(pcl::PointXYZ point,int id,int class_num);
int get_class(std::vector<darknet_ros_msgs::BoundingBox>::iterator);

//constructor
Fusion::Fusion(){
  ROS_INFO("fusion initializing");
  p_pcl = pcl::PointCloud<pcl::PointXYZ>::Ptr
   (new pcl::PointCloud<pcl::PointXYZ>);
  ROS_INFO("fusion initialized");
}

//gets pcl2 message and converts to pcl<pclXYZRGBA>
void Fusion::pcl2_callback(const sensor_msgs::PointCloud2ConstPtr& pcl2_msg){
  pcl::fromROSMsg(*pcl2_msg,*this->p_pcl);
  ROS_INFO("callback pcl2");
  printf("heigt: %d\nwidth: %d\n",p_pcl->height,p_pcl->width);
  // for(int i=300;i<500;i++){
  //   p_pcl->points
  // }
}

void Fusion::bb_callback(const darknet_ros_msgs::BoundingBoxesPtr& bb_msg){
  ROS_INFO("callback bouding box");
  markerArray.markers.clear();
  pcl::PointXYZ new_point;
  int id = 0, class_num;
  visualization_msgs::Marker new_marker;
  for(auto it=bb_msg->bounding_boxes.begin(); it<bb_msg->bounding_boxes.end();it++){
      new_point = get_point(it,p_pcl);
      class_num = get_class(it);
      new_marker = create_marker(new_point,id,class_num);
      markerArray.markers.push_back(new_marker);
      id++;
  }
  ROS_INFO("marker array size %d",markerArray.markers.size());
}

// //gets vector of bb from darknet
// //for each element in bb array get subarray of points in bb
// void Fusion::bb_callback(const darknet_ros_msgs::BoundingBoxesPtr& bb_msg){
//  for(auto it = bb_msg->bounding_boxes.begin(); it != bb_msg->bounding_boxes.end(); it++){
//   cv_lidar_fusion_pkg::relative_obstaclePtr new_point;  
//   new_point = get_bb_pos(it);
//   update_obst_arr(new_point);
//  }
// }

// //gets pos of bouy at bb with statistical function parameter (i.e. min, avg, median)
// cv_lidar_fusion_pkg::relative_obstaclePtr 
//     Fusion::get_bb_pos(std::vector<darknet_ros_msgs::BoundingBox>::iterator bb){
//       cv_lidar_fusion_pkg::relative_obstaclePtr new_point(new cv_lidar_fusion_pkg::relative_obstacle);
//       pcl::PointCloud<pcl::PointXYZRGBA>::VectorType subarray = Fusion::bb_to_subarray(bb,this->p_pcl);
//       new_point = Fusion::point_from_subarray(subarray,this->func_param);
//       return new_point;
//     }

// //update relative obstacles array and time stamp
// void Fusion::update_obst_arr(cv_lidar_fusion_pkg::relative_obstaclePtr){
  
// }

//function that gets avarage point from pcl with bb data
// pcl::PointCloud<pcl::PointXYZ>::VectorType Fusion::get_point(std::vector<darknet_ros_msgs::BoundingBox> boundingboxs,const pcl::PointCloud<pcl::PointXYZ>::Ptr p_pcl ){
//   std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>> subarray;
//   std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>> subarray2;
//   pcl::PointXYZ av_point;
//   markerArray.markers.clear();
//   std::vector<darknet_ros_msgs::BoundingBox>::iterator bb = boundingboxs.begin();
//   for(int y=bb->ymin;y<bb->ymax;y++){
//     for(int x=bb->xmin;x<bb->xmax;x++){
//       if(!check_nan_inf(p_pcl->points[y*p_pcl->width + x])) continue;
//       subarray.push_back(p_pcl->points[y*p_pcl->width + x]);
//       //printf("(%f,%f,%f) ",subarray.back().x,subarray.back().y,subarray.back().z);
//     }
//   }
//   av_point = avg_point(subarray);
  
//   //printf("\n(%f,%f,%f)\n",av_point.x,av_point.y,av_point.z);
//   red_marker->header.stamp = ros::Time();
//   red_marker->pose.position.x = av_point.x;
//   red_marker->pose.position.y = av_point.y;
//   red_marker->pose.position.z = av_point.z;
//   markerArray.markers.push_back(*red_marker);
//   if(bb>=boundingboxs.end()){
//     return subarray;
// }

//   for(int y=bb->ymin;y<bb->ymax;y++){
//     for(int x=bb->xmin;x<bb->xmax;x++){
//       if(!check_nan_inf(p_pcl->points[y*p_pcl->width + x])) continue;
//       subarray2.push_back(p_pcl->points[y*p_pcl->width + x]);
//       //printf("(%f,%f,%f) ",subarray.back().x,subarray.back().y,subarray.back().z);
//     }
//   }
//   av_point = avg_point(subarray2);
//   //printf("\n(%f,%f,%f)\n",av_point.x,av_point.y,av_point.z);
//   green_marker->header.stamp = ros::Time();
//   green_marker->pose.position.x = av_point.x;
//   green_marker->pose.position.y = av_point.y;
//   green_marker->pose.position.z = av_point.z;
//   markerArray.markers.push_back(*green_marker);
//   return subarray;
// }


pcl::PointXYZ 
Fusion::get_point(std::vector<darknet_ros_msgs::BoundingBox>::iterator boundingbox,
const pcl::PointCloud<pcl::PointXYZ>::Ptr p_pcl){
    std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>> subarray;
    pcl::PointXYZ av_point;
    for(int y = boundingbox->ymin;y<boundingbox->ymax;y++){
      for(int x = boundingbox->xmin;x<boundingbox->xmax;x++){
        if(!check_nan_inf(p_pcl->points[y*p_pcl->width + x])) continue;
        subarray.push_back(p_pcl->points[y*p_pcl->width + x]);
      }
    }
    //printf("ymin: %f ymax: %f\nxmin: %f xmax: %f ",boundingbox->ymin,boundingbox->ymax,boundingbox->xmin, boundingbox->xmax );

      return avg_point(subarray);
}

// //statistical analisys of bb subarray to get new relative point
// //add ros param to inputs
// cv_lidar_fusion_pkg::relative_obstaclePtr Fusion::point_from_subarray(pcl::PointCloud<pcl::PointXYZRGBA>::VectorType subarray, std::string func_param){
// }

bool check_nan_inf(pcl::PointXYZ point){
  int x = std::fpclassify(point.x);
  int y = std::fpclassify(point.y);
  int z = std::fpclassify(point.z);
  if(x == FP_NAN || x == FP_INFINITE ||
     y == FP_NAN || y == FP_INFINITE ||
     z == FP_NAN || z == FP_INFINITE) return false;
  else{
    return true;
  }
}

pcl::PointXYZ avg_point(std::vector<pcl::PointXYZ, Eigen::aligned_allocator<pcl::PointXYZ>> subarray)
{
  int size = subarray.size();
  float avg_x = 0.0, avg_y = 0.0, avg_z = 0.0;
  pcl::PointXYZ av_point;
  for(int i = 0; i < size; i ++)
  {
    avg_x += subarray[i].x;
    avg_y += subarray[i].y;
    avg_z += subarray[i].z;
  }
  av_point.x = avg_x / size;
  av_point.y = avg_y / size;
  av_point.z = avg_z / size;
  return av_point;

}

//create new marker
visualization_msgs::Marker create_marker(pcl::PointXYZ point,int id,int class_num){
  visualization_msgs::Marker marker;
  marker.header.frame_id = "zed2_left_camera_center";
  marker.header.stamp = ros::Time();
  marker.ns = "bouys";
  marker.id = id;
  marker.color.a = 1.0;
  
  //determine shape of marker
  if(class_num == 3 || class_num == 5){
    marker.type = visualization_msgs::Marker::CYLINDER;
    marker.scale.z = 0.9;}
  else if(class_num == 6){
    marker.type = visualization_msgs::Marker::CUBE;
    marker.scale.z = 0.2;}
  else{
    marker.type = visualization_msgs::Marker::SPHERE;
    marker.scale.z = 0.2;}
  marker.action = visualization_msgs::Marker::ADD;
  marker.pose.orientation.x = 0.0;
  marker.pose.orientation.y = 0.0;
  marker.pose.orientation.z = 0.0;
  marker.pose.orientation.w = 1.0;
  marker.scale.x = 0.2;
  marker.scale.y = 0.2;
  
  if (class_num == 0){
    marker.color.r = 0.0;
    marker.color.g = 0.0;
    marker.color.b = 0.0;}
  else if (class_num == 1){
    marker.color.r = 0.0;
    marker.color.g = 0.0;
    marker.color.b = 1.0;}
  else if (class_num == 2 || class_num == 3){
    marker.color.r = 0.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;}
  else if (class_num == 4 || class_num == 5){
    marker.color.r = 1.0;
    marker.color.g = 0.0;
    marker.color.b = 0.0;}
  else if (class_num == 6){
    marker.color.r = 0.5;
    marker.color.g = 0.5;
    marker.color.b = 0.5;}
  else if (class_num == 7){
    marker.color.r = 1.0;
    marker.color.g = 1.0;
    marker.color.b = 0.0;}

  marker.pose.position.x = point.x;
  marker.pose.position.y = point.y;
  marker.pose.position.z = point.z;
  return marker;
}

int get_class(std::vector<darknet_ros_msgs::BoundingBox>::iterator bb){
    if (bb->Class[0]=='B' && bb->Class[2]=='a')
      return 0; // Black ball
    if (bb->Class[0]=='B' && bb->Class[2]=='u')
      return 1; // Blue ball
    if (bb->Class[0]=='G' && bb->Class[6]=='b')
      return 2; // Green ball
    if (bb->Class[0]=='G' && bb->Class[6]=='p')
      return 3; // Green pole
    if (bb->Class[0]=='R' && bb->Class[4]=='b')
      return 4; // Red ball
    if (bb->Class[0]=='R' && bb->Class[4]=='p')
      return 5; // Red pole
    if (bb->Class[0]=='X')
      return 6; // X target
    if (bb->Class[0]=='Y')
      return 7; // Yellow ball
}