#!/usr/bin/env python

import rospy
import random
from cv_lidar_fusion_pkg.msg import relative_obstacle, relative_obstacles
from rosgraph_msgs.msg import Clock
from rospy.topics import Subscriber
CLASS_TYPES =["green bouy", "Red Marker", "blue Marker", "Yellow bouy", "None"]
OBSTACLES_TO_GENERATE = 15
MAX_OBSTACLE_COUNT = 25
class SimClock():
  def __init__(self, *args, **kwds):
    self.clock_obj = Clock()
    rospy.loginfo("clock created:\n{}".format(self.clock_obj))
  def clock_callback(self,msg):
    self.clock_obj = msg
  
  def sim_clock_sub(self):
    sub = Subscriber("clock",Clock,callback=self.clock_callback)

sim_clock = SimClock()

def generate_obstacle(current_time):
  print(current_time)
  obst = relative_obstacle()
  obst.point.header.frame_id = "base_link"
  obst.id = random.randint(1,MAX_OBSTACLE_COUNT)
  obst.point.header.stamp = current_time
  obst.Class = CLASS_TYPES[random.randint(0,4)]
  obst.point.point.x = float(random.randrange(0,150))/10
  obst.point.point.y = float(random.randrange(0,150))/10
  return obst

def obst_pub():
  pub = rospy.Publisher("fusion/relative_obstacles",relative_obstacles,queue_size=10,latch=True)
  rate = rospy.Rate(10)
  obst_arr = relative_obstacles()
  obst_arr.header.frame_id = "base_link"
  obst_arr.obstacle_array = []
  
  for i in range(OBSTACLES_TO_GENERATE):
    now = sim_clock.clock_obj.clock
    obst = generate_obstacle(now) 
    obst_arr.obstacle_array.append(obst)


  obst_arr.header.stamp = sim_clock.clock_obj.clock
  pub.publish(obst_arr)
  while not rospy.is_shutdown():
    try:
      rospy.sleep(1)
    except KeyboardInterrupt("exiting node keyboard interrupt"):
      exit()


if __name__ == "__main__":
  rospy.init_node("random_obstacles",anonymous=True)
  rospy.loginfo("random obstacle publisher node started")
  sim_clock.sim_clock_sub()
  rospy.sleep(2)
  obst_pub()