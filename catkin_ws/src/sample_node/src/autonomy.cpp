#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

class StateMachine
{
  public:
    StateMachine()
    {
      //Topic you want to publish
      pub = nh.advertise<std_msgs::String>("/autonomy_out", 1);

      //Topic you want to subscribe
      sub = nh.subscribe("/spam", 1, &StateMachine::callback, this);
    }

    void callback(const std_msgs::String::ConstPtr& msg)
    {
      std_msgs::String output;
      std::stringstream outstream;
      outstream << "Autonomy got: " << msg->data;
      output.data = outstream.str();

      ROS_INFO("%s", output.data.c_str());
      pub.publish(output);
    }

  private:
    ros::NodeHandle nh; 
    ros::Publisher pub;
    ros::Subscriber sub;

}; // End of class StateMachine

int main(int argc, char **argv)
{
  //Initiate ROS
  ros::init(argc, argv, "autonomy");

  //Create an object of class StateMachine that will take care of everything
  StateMachine SMObject;

  ros::spin();

  return 0;
}