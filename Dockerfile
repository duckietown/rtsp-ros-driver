FROM duckietown/rpi-ros-kinetic-base:master19-no-arm

RUN mkdir /home/camera_driver
COPY . /home/camera_driver
RUN /bin/bash -c "cd /home/camera_driver/ && source /opt/ros/kinetic/setup.bash && catkin_make -j -C catkin_ws/"

CMD /bin/bash -c "source /opt/ros/kinetic/setup.bash ; source /home/camera_driver/catkin_ws/devel/setup.bash; export ROS_IP=172.31.168.110; export ROS_HOSTNAME=172.31.168.110; export ROS_MASTER_URI="http://172.31.168.115:11311"; roslaunch rtsp_ros_driver rtsp_driver_node.launch"
