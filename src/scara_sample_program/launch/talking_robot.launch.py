from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    
    task_server_node = Node(
        package="scara_sample_program",
        executable="task_server_node"
    )
    
    scara_alexa_node = Node(
        package = "scara_sample_program",
        executable="scara_alexa.py"
    )
    
    return LaunchDescription([
        task_server_node,
        scara_alexa_node
    ])