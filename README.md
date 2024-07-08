# ROS2-driver-for-mitsubishi-RH-6FRH-robot
This is a ROS2 driver for MELFA RH-6FRH robot compatible with CR800 controller

To use the driver first isntall ROS2 humble on your computer.
The instruction to install the ROS2 humble can be found in the link below:

https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

After succesfully installing ROS2 humble, it is required to install some necessary packages. Without them, you won't be able to run the driver.
Use commands below to install all the required packages:

sudo apt-get install ros-humble-joint-state-publisher-gui

sudo apt-get install ros-humble-xacro

sudo apt-get install ros-humble-gazebo-ros

sudo apt-get install ros-humble-ros2-control

sudo apt-get install ros-humble-ros2-controllers

sudo apt-get install ros-humble-gazebo-ros2-control

sudo apt-get install ros-humble-moveit

After installing all the packages use this command:

echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc

And configure the python:

sudo apt-get install python3-pip

After finishing all the installation, the driver is ready to use. To use the driver open the MTS-RH6FRH_ROS2_DRIVER.

Source the workspace using command below:

source /opt/ros/humble/setup.bash

Use the colcon build

Now source the workspace using command below:

. install/setup.bash

After succesfully using all those commands you can launch the driver.

To use the driver in simulation mode use the command below:

ros2 launch robot_bringup simulation.launch.py

To use the driver with a real robot use the command below:

ros2 launch robot_bringup real_robot.launch.py

The default robot ip set in the driver is 192.168.0.20 

To change the ip you can edit the "scara.config.xacro" file in robot_description/config folder.

WARNING!!!!! After executing the move path the robot will start moving. Make sure that the working environment is safe and no people are tanding on robot's way.
