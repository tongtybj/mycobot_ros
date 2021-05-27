#!/usr/bin/env python2
# license removed for brevity


import rospy
from rospy.timer import sleep
from visualization_msgs import msg
from visualization_msgs.msg import Marker
# from pymycobot.mycobot import MyCobot
# from pymycobot.genre import Coord
# from pymycobot import PI_PORT, PI_BAUD # For raspberry pi version of mycobot.
import time
from mycobot_ros.srv import (
    GetCoords, SetCoords, GetAngles, SetAngles, PumpStatus)


set_coords = None
set_angles = None
toggle_pump = None



x_offset = 15
y_offset = 30
z_offset = 100

flag = False


def grippercallback(data):
    global flag
    print(type(data))
    # rospy.loginfo('gripper_subscriber get date :%s', data)
    # print(Marker.)
    # coord_datas = mc.get_coords()
    # print(coord_datas)
    if flag:
        return


    # pump lenght: 88mm
    x = float(format(data.pose.position.x*1000, '.2f'))
    y = float(format(data.pose.position.y*1000, '.2f'))
    z = float(format(data.pose.position.z*1000, '.2f'))


    print(x, y, z)

    # detect heigth + pump height + limit height + offset
    x += x_offset
    y += y_offset
    z = z  + 88 + 25 + z_offset


    set_coords(x, y, z, -175, 0, -90, 70, 2)
    time.sleep(2.5)

    for i in range(1,5):

        set_coords(x, y, z - i * 10, -175, 0, -90, 15, 2)
        time.sleep(.3)

    time.sleep(2)


    toggle_pump(1)
    # pump on

    set_coords(x, y, z + 20, -165, 0, -90, 70, 2)
    time.sleep(1.5)

    set_angles(0, 30, -50, -40, 0, 0, 50)
    time.sleep(1.5)

    put_z = 140
    set_coords(39.4, -174.7, put_z ,-177.13, -4.13, -152.59,70,2)
    time.sleep(1.5)

    for i in range (1,5):
        set_coords(39.4, -174.7, put_z-i*20, -177.13, -4.13, -152.59,15,2)
        time.sleep(.3)

    toggle_pump(0)

    set_angles(0, 30, -50, -40, 0, 0, 50)
    time.sleep(1.5)

    # finally
    flag = True

def gipper_subscriber():
    global set_coords, set_angles, toggle_pump
    # rospy.wait_for_service('get_joint_angles')
    rospy.wait_for_service('set_joint_angles')
    # rospy.wait_for_service('get_joint_coords')
    rospy.wait_for_service('set_joint_coords')
    rospy.wait_for_service('switch_pump_status')
    try:
        # get_coords = rospy.ServiceProxy('get_joint_coords', GetCoords)
        set_coords = rospy.ServiceProxy('set_joint_coords', SetCoords)
        # get_angles = rospy.ServiceProxy('get_joint_angles', GetAngles)
        set_angles = rospy.ServiceProxy('set_joint_angles', SetAngles)
        toggle_pump =rospy.ServiceProxy('switch_pump_status', PumpStatus)
    except:
        print('start error ...')
        exit(1)

 
    set_angles(0, 30, -50, -40, 0, 0, 50)

    time.sleep(2.5)
    rospy.init_node('gipper_subscriber',anonymous=True)
    rospy.Subscriber('visualization_marker',Marker,grippercallback, queue_size=1)
    print 'gripper test'
    rospy.spin()

    
    

if __name__ == '__main__':
    gipper_subscriber()
    