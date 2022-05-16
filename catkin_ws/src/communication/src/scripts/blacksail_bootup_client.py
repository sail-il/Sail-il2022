import rospy
import paramiko
import sys
import argparse
from std_msgs.msg import String
from std_srvs.srv import Trigger

if __name__ == '__main__':
    parser =argparse.ArgumentParser(description="start gpu")
    parser.add_argument('gpu', default="blacksail")
    args = vars(parser.parse_args())
    gpu = args["gpu"]
    gpu_list=[]
    serv_list=[]
    
    ssh = paramiko.SSHClient()
    ssh.connect("192.168.1.51", username="blacksail", password="sail2021")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("roscore")    
    
    rospy.init_node("/launch_Srv")
    
    if (gpu == "all"):
        gpu_list = ["blacksail","greensail","whitesail"]
    else:
        gpu_list.append[gpu]
    
    for i in range(len(gpu_list)):
        serv_name = ("/"+ gpu_list[i]+ "_launch")    
        serv_list[i] = rospy.wait_for_service(serv_name)
        try:
            trig = rospy.ServiceProxy(serv_name, Trigger)
            #TODO- make a srv with params that can have several bootup options.
            status = trig()
            if status.success:
                rospy.loginfo("\n" + gpu_list[i] +" launch succes!\n")
            else :
                rospy.loginfo("\n" + gpu_list[i] +" launch failed!\n reason:"+ status.message)
        
        
        except rospy.ServiceException as e:
            rospy.logwarn("Service failed. reason :" + str(e))
        