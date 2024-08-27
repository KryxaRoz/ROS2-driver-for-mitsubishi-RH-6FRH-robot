# ROS2-driver-for-mitsubishi-RH-6FRH-robot

This is a ROS2 driver for MELFA RH-6FRH robot compatible with the CR800 controller.

## Installation Instructions

### 1. Install ROS2 Humble

To use the driver, first install ROS2 Humble on your computer. The instructions can be found at the link below:

[ROS2 Humble Installation Guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

### 2. Install Required Packages

After successfully installing ROS2 Humble, you need to install some necessary packages. Without them, you won't be able to run the driver. Use the commands below to install all the required packages:
```bash
sudo apt-get install ros-humble-joint-state-publisher-gui
sudo apt-get install ros-humble-xacro
sudo apt-get install ros-humble-gazebo-ros
sudo apt-get install ros-humble-ros2-control
sudo apt-get install ros-humble-ros2-controllers
sudo apt-get install ros-humble-gazebo-ros2-control
sudo apt-get install ros-humble-moveit
```

### 3. Configure the Environment
After installing all the packages, use this command to configure your environment:
```bash
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
```
### 4. Configure Python
Install Python pip if it’s not already installed:
```bash
sudo apt-get install python3-pip
```
### 5. Source the ROS2 Workspace
After finishing all the installations, the driver is ready to use. To begin, open the MTS-RH6FRH_ROS2_DRIVER workspace.

Source the workspace using the command below:
```bash
source /opt/ros/humble/setup.bash
```
Then build the workspace with:
```bash
colcon build
```
After building, source the workspace:
```bash
. install/setup.bash
```
### 6. Launch the Driver
After successfully executing all these commands, you can launch the driver.

To use the driver in simulation mode, use the command below:
```bash
ros2 launch robot_bringup simulation.launch.py
```
To use the driver with a real robot, use the command below:
```bash
ros2 launch robot_bringup real_robot.launch.py
```
## Robot Configuration
The robot program to use the driver requires the MXT instruction:
```bash
Open "ENET:192.168.0.20" As #1
MXT 1,1,100
```
The default robot IP set in the driver is 192.168.0.20.

To change the IP, you can edit the scara.config.xacro file located in the robot_description/config folder.

### Important Safety Warning
WARNING!!! After executing the move path, the robot will start moving. Ensure that the working environment is safe and that no people are standing in the robot's path.
