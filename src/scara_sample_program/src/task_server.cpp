#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <scara_msgs/action/task.hpp>
#include <rclcpp_components/register_node_macro.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

#include <memory>
#include <thread>

using namespace std::placeholders;

namespace scara_sample_program
{
    class TaskServer : public rclcpp::Node
    {
    public:
        explicit TaskServer(const rclcpp::NodeOptions& options = rclcpp::NodeOptions()) 
        : Node("task_server", options)
        {
            action_server_ = rclcpp_action::create_server<scara_msgs::action::Task>(
                this, "task_server", 
                std::bind(&TaskServer::goalCallback, this, _1, _2),
                std::bind(&TaskServer::cancelCallback, this, _1),
                std::bind(&TaskServer::acceptedCallback, this, _1)
            );

            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Starting the Action Server");
        }

    private:
        rclcpp_action::Server<scara_msgs::action::Task>::SharedPtr action_server_;

        rclcpp_action::GoalResponse goalCallback(const rclcpp_action::GoalUUID& uuid, std::shared_ptr<const scara_msgs::action::Task::Goal> goal)
        {
            RCLCPP_INFO_STREAM(rclcpp::get_logger("rclcpp"), "Received goal request with id: " << goal->task_number);
            return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
        }

        void acceptedCallback(const std::shared_ptr<rclcpp_action::ServerGoalHandle<scara_msgs::action::Task>> goal_handle)
        {
            std::thread{std::bind(&TaskServer::execute, this, _1), goal_handle}.detach();
        }

        void execute(const std::shared_ptr<rclcpp_action::ServerGoalHandle<scara_msgs::action::Task>> goal_handle)
        {
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Executing goal");
            auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");

            std::vector<double> arm_joint_goal;

            if(goal_handle->get_goal()->task_number == 0)
            {
                arm_joint_goal = {0.0, 0.0, 150.0, 0.0};
            }
            else if(goal_handle->get_goal()->task_number == 1)
            {
                arm_joint_goal = {0.52, -0.52, 220.0, 1.14};
            }
            else if(goal_handle->get_goal()->task_number == 2)
            {
                arm_joint_goal = {-0.52, 0.52, 300.0, -1.14};
            }
            else
            {
                RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Invalid Task Number");
                return;
            }

            bool arm_within_bounds = arm_move_group.setJointValueTarget(arm_joint_goal);

            if(!arm_within_bounds)
            {
                RCLCPP_WARN(rclcpp::get_logger("rclcpp"), "Target joint position outside the limit!");
                return;
            }

            moveit::planning_interface::MoveGroupInterface::Plan arm_plan;

            bool arm_plan_success = arm_move_group.plan(arm_plan) == moveit::core::MoveItErrorCode::SUCCESS;

            if(arm_plan_success)
            {
                RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Planner Succeed, moving the arm");
                arm_move_group.move();
            }
            else
            {
                RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Planner failed");
                return;
            }

            auto result = std::make_shared<scara_msgs::action::Task::Result>();
            result->success = true;
            goal_handle->succeed(result);
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Goal succeeded");
        }

        rclcpp_action::CancelResponse cancelCallback(const std::shared_ptr<rclcpp_action::ServerGoalHandle<scara_msgs::action::Task>> goal_handle)
        {
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "Received request to cancel the goal");
            auto arm_move_group = moveit::planning_interface::MoveGroupInterface(shared_from_this(), "arm");

            arm_move_group.stop();

            return rclcpp_action::CancelResponse::ACCEPT;
        }
    };
}

RCLCPP_COMPONENTS_REGISTER_NODE(scara_sample_program::TaskServer)