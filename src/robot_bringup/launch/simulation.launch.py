# Description: This file is a launch file which activates the ROS2 driver for the simulated RH-6FRH5520 robot arm.
# WARNING!!!! Do not use the driver with any other robot arm.
# Mitsubishi Electric assume any liability if the driver is used with a different robot
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
import os
def generate_launch_description():
    
    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robot_description"),
            "launch",
            "gazebo.launch.py"
        )
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robot_controllers"),
            "launch",
            "controllers.launch.py"
        ),
        launch_arguments={"is_sim" : "True"}.items()
    )
    
    moveit = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("robot_moveit"),
            "launch",
            "moveit.launch.py"
        ),
        launch_arguments={"is_sim" : "True"}.items()
    )
    
    return LaunchDescription([
        gazebo,
        controller,
        moveit
    ])