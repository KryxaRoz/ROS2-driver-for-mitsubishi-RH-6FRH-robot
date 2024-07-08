// Description: This file is a header file for RH-6FRH5520 hardware interface file.
// WARNING!!!! Do not use the driver with any other robot arm.
// Mitsubishi Electric assume any liability if the driver is used with a different robot

#ifndef RH6FRH_HARDWARE__RH6FRH_JOINT_HW_HPP_
#define RH6FRH_HARDWARE__RH6FRH_JOINT_HW_HPP_

#include <rclcpp/rclcpp.hpp>
#include <hardware_interface/system_interface.hpp>
#include <rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp>
#include <rclcpp_lifecycle/state.hpp>
#include <hardware_interface/handle.hpp>
#include <hardware_interface/hardware_info.hpp>
#include <hardware_interface/system_interface.hpp>
#include <hardware_interface/types/hardware_interface_return_values.hpp>
#include <hardware_interface/types/hardware_interface_type_values.hpp>
#include "robot_hardware/rh6frh_protocol.h"



#include <rclcpp/macros.hpp>

#include <vector>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <string>


namespace rh6frh_hardware
{
using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;
class Rh6frhHardwareInterface : public hardware_interface::SystemInterface
{
public:
    RCLCPP_SHARED_PTR_DEFINITIONS(Rh6frhHardwareInterface);

    //RH6FRH_HARDWARE_PUBLIC
    CallbackReturn on_init(const hardware_interface::HardwareInfo & hardware_info) override;

    //RH6FRH_HARDWARE_PUBLIC
    std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

    //RH6FRH_HARDWARE_PUBLIC
    std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

    //RH6FRH_HARDWARE_PUBLIC
    CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;

    //RH6FRH_HARDWARE_PUBLIC
    CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;

    // RH6FRH_HARDWARE_PUBLIC
    hardware_interface::return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;

    //RH6FRH_HARDWARE_PUBLIC
    hardware_interface::return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;

private:
    //communication parameters
    int sock_;
    struct sockaddr_in destSockAddr_;
    SOCKET destSocket_;
    MXTCMD MXTsend_, MXTrecv_;
    unsigned long counter_;
    int socket_status_;
    //Control and state variables
    std::vector<double> hw_commands_;
    std::vector<double> hw_states_;
};
}
#endif