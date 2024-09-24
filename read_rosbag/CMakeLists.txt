cmake_minimum_required(VERSION 3.5.0)
project(read_rosbag VERSION 0.1.0 LANGUAGES C CXX)

find_package(catkin REQUIRED COMPONENTS
    roscpp
    rosbag_storage
)

include_directories(include ${catkin_INCLUDE_DIRS})
add_executable(read_rosbag main.cpp)
target_link_libraries(read_rosbag ${catkin_LIBRARIES})
