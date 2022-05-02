#!/usr/bin/env python2.7

import rospy
from telemtry.srv import bool


def handle_shutdown_button(req):
    engine_status = rospy.get_param("Engine_Status")
    if req.active != True or engine_status == 0:
        return False
    else: #turn off engines
        ##call for control code to turn off engines
        rospy.set_param("Engine_Status", 0)


if __name__ == '__main__':
    rospy.init_node("/Engine_Shutdown_Srv")

    service = rospy.Service("/Engine_Shutdown", bool, handle_shutdown_button)
