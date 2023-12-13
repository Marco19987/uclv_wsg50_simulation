
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument 
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory('uclv_wsg50_simulation'),
        'urdf',
        'wsg50.urdf.xacro'
    )
    rviz_config = os.path.join(
        get_package_share_directory('uclv_wsg50_simulation'),
        'rviz',
        'display_gripper.rviz'
    )

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("uclv_wsg50_simulation"), "urdf/", LaunchConfiguration("model")]),
            ""
        ]
    )

    return LaunchDescription([
        # Declare the URDF parameters
        DeclareLaunchArgument('model', default_value=urdf_file),
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('rvizconfig', default_value=rviz_config),

        # Publish static robot state
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{"robot_description": robot_description_content}]
            #parameters=[{'use_gui': LaunchConfiguration('gui')}],
            #arguments=[urdf_file]
        ),

        # Joint state publisher
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher',
            output='screen',
        ),

        # RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz',
            output='screen',
            arguments=['-d', rviz_config]
        )
    ])
