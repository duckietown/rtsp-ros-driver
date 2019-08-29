#! /usr/bin/env python2

import cv2
import rospy
import thread
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import String

class Camera(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        # get ROS parameters
        self.resource = rospy.get_param('~rtsp_resource')
        self.new_resource = ""
        self.image_topic = rospy.get_param('~image_topic')
        # open RTSP stream
        self.cap = cv2.VideoCapture(self.resource)
        if not self.cap.isOpened():
            rospy.logerr("Error opening resource `%s`. Please check." % self.resource)
            exit(0)
        rospy.loginfo("Resource successfully opened")

        # create publishers
        self.image_pub = rospy.Publisher(self.image_topic, CompressedImage, queue_size=1)
        self.camera = rospy.Subscriber("~camera_switch", String, self.camera_switch_cb, queue_size=1)

        # initialize ROS_CV_Bridge
        self.ros_cv_bridge = CvBridge()
        self.change = False
        self.is_shutdown = False

    def startCapturing(self):
        # initialize variables
        print "Correctly opened resource, starting to publish feed."
        rval, cv_image = self.cap.read()

        # process frames
        while rval:
            if self.change:
                rospy.loginfo("Change now")
                self.cap.release()
                self.resource = self.new_resource
                self.cap = cv2.VideoCapture(self.resource)
                self.change = False
                rospy.loginfo("Changed")
            # get new frame
            rval, cv_image = self.cap.read()
            # handle Ctrl-C
            key = cv2.waitKey(20)
            if rospy.is_shutdown() or self.is_shutdown or key == 27 or key == 1048603:
                break
            # convert CV image to ROS message
            image_msg = self.ros_cv_bridge.cv2_to_compressed_imgmsg(cv_image)
            image_msg.header.stamp = rospy.Time.now()
            self.image_pub.publish( image_msg )

    def camera_switch_cb(self, data):
        rospy.loginfo(data.data)
        self.new_resource = data.data
        self.change = True

    def onShutdown(self):
        rospy.loginfo("[%s] Closing ip camera." % (self.node_name))
        self.is_shutdown = True
        rospy.loginfo("[%s] Shutdown." % (self.node_name))


if __name__ == '__main__':
    # initialize ROS node
    print "Initializing ROS node... ",
    rospy.init_node('rtsp_camera_driver_node', anonymous=False)
    print "Done!"
    ip_cam_node = Camera()
    rospy.on_shutdown(ip_cam_node.onShutdown)
    thread.start_new_thread(ip_cam_node.startCapturing, ())

    rospy.spin()
