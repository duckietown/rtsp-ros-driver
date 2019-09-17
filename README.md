# rtsp_ros_driver

This ROS package contains a driver node that reads frames from an RTSP video stream (e.g., IP Camera) and publishes them out as [sensor_msgs/CompressedImage](http://docs.ros.org/api/sensor_msgs/html/msg/CompressedImage.html) ROS messages.
Different url's of IP cam's can be switched between via the switch callback.
