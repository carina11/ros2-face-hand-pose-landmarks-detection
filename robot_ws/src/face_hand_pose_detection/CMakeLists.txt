cmake_minimum_required(VERSION 3.8)
project(face_hand_pose_detection)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

install(DIRECTORY
  face_hand_pose_detection
  launch
  params
  DESTINATION share/${PROJECT_NAME}/
)

### Python support ###
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
# Install Python executables
install(PROGRAMS
  face_hand_pose_detection/face_hand_pose_detection_node.py

  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
