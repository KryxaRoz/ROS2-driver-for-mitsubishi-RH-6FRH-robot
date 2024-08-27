# Description: This file is a launch file to display the 3D model of a RH-6FRH5520 in RVIZ2 with joint state broadcaster.
# WARNING!!!! Do not use the driver with any other robot arm.
# Mitsubishi Electric assume any liability if the driver is used with a different robot

from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(get_package_share_directory("robot_description"),"config","scara.config.xacro"),
        description="Absolute path to the robot URDF file"
        )
    
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("model")]))

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description" : robot_description}]
    )

    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", os.path.join(get_package_share_directory("robot_description"),"rviz","scara.rviz")]
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz2_node
    ])