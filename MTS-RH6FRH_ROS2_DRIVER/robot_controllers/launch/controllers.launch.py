# Description: This file is a launch file which activates the defined ROS2 controllers for RH-6FRH5520 robot.
# WARNING!!!! Do not use the driver with any other robot arm.
# Mitsubishi Electric assume any liability if the driver is used with a different robot
from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command,LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.conditions import UnlessCondition

def generate_launch_description():
    
    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )
    
    is_sim = LaunchConfiguration("is_sim")
     
    robot_description = ParameterValue(
        Command(
        [
            "xacro ",
            os.path.join(get_package_share_directory("robot_description"),"config","scara.config.xacro"),
            " is_sim:=False"
        ]    
        ),
        value_type=str
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description" : robot_description}],
        condition=UnlessCondition(is_sim)
    )
    
    controller_manager= Node (
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description,
             "use_sim_time": is_sim},
            os.path.join(get_package_share_directory("robot_controllers"),"config","scara_controllers.yaml")
        ],
        condition=UnlessCondition(is_sim)
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ]
    )

    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
        ]
    )

    return LaunchDescription([
        is_sim_arg,
        robot_state_publisher,
        controller_manager,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
    ])