#include <iostream>
#include <fstream>

#include "rosbag/bag.h"
#include <rosbag/view.h>
#include <rosbag/query.h>
#include <nav_msgs/Path.h>
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/Point.h>

int main() {
    rosbag::Bag bag;
    std::string bag_path = "../test.bag";
    bag.open(bag_path, rosbag::bagmode::Read);

    if (!bag.isOpen()) {
        std::cout << "Bag file not opened" << std::endl;
        return -1;
    }

    std::set<std::string> topics;
    std::set<std::string> data_types;

    // Collect all topics, data types
    for (rosbag::MessageInstance m : rosbag::View(bag))
    {
        topics.insert(m.getTopic());
        data_types.insert(m.getDataType());
    }

    std::cout << "Topics: " << std::endl;
    for (const auto& topic : topics) {
        std::cout << topic << std::endl;
    }
    std::cout << std::endl;

    // Save plan to csv
    rosbag::View view_plan(bag, rosbag::TopicQuery("/move_base/LinearPlanner/global_plan"));
    std::ofstream plan_path("../plan_path.csv");
    plan_path << "x,y" << std::endl;
    for (rosbag::MessageInstance m : view_plan) {
        nav_msgs::Path::ConstPtr i = m.instantiate<nav_msgs::Path>();
        if (i != nullptr) {
            for (auto p : i.get()->poses) {
                plan_path << p.pose.position.x << "," << p.pose.position.y << std::endl;
            }
        }
    }

    // Save path from odometry to csv
    rosbag::View view_odom(bag, rosbag::TopicQuery("/odometry/filtered_odom"));
    std::ofstream path("../path.csv");
    path << "x,y" << std::endl;
    for (rosbag::MessageInstance m : view_odom) {
        nav_msgs::Odometry::ConstPtr i = m.instantiate<nav_msgs::Odometry>();
        if (i != nullptr) {
            path << i.get()->pose.pose.position.x << "," << i.get()->pose.pose.position.y << std::endl;
        }
    }

    bag.close();
    return 0;
}
