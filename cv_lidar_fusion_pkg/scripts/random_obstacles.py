#!/usr/bin/env python

import rospy
import random
from cv_lidar_fusion_pkg.msg import relative_obstacle, relative_obstacles
from rosgraph_msgs.msg import Clock
CLASS_TYPES =["green bouy", "Red Marker", "blue Marker", "Yellow bouy", "None"]
def generate_obstacle():
  obst = relative_obstacle()
  obst.point.header.frame_id = "base_link"
  obst.id = random.randint(1,25)
  obst.Class = CLASS_TYPES[random.randint(0,4)]
  obst.point.point.x = float(random.randrange(0,150))/10
  obst.point.point.y = float(random.randrange(0,150))/10
  return obst

def obst_pub(now):
  
  pub = rospy.Publisher("fusion/relative_obstacles",relative_obstacles,queue_size=10)
  rate = rospy.Rate(0.5)
  obst_arr = relative_obstacles()
  obst_arr.header.frame_id = "base_link"
  obst_arr.obstacle_array = []
  
  for i in range(5):
    obst = generate_obstacle() 
    obst_arr.obstacle_array.append(obst)
  while not rospy.is_shutdown():
    print(current_time)
    for item in obst_arr.obstacle_array:
      item.point.header.stamp = now.clock
    obst_arr.header.stamp = now.clock
    pub.publish(obst_arr)
    rate.sleep()

def clock_sub(time_obj):
  rate = rospy.Rate(20)
  clock_sub = rospy.Subscriber("/clock",Clock,callback=get_time,callback_args=[time_obj])
  rate.sleep()

def get_time(msg,args):
  args[0].clock.secs = msg.clock.secs
  args[0].clock.nsecs = msg.clock.nsecs
  

if __name__ == "__main__":
  rospy.init_node("random_obstacles",anonymous=True)
  rospy.loginfo("random obstacle publisher node started")
  current_time = Clock()
  clock_sub(current_time)
  obst_pub(current_time)


