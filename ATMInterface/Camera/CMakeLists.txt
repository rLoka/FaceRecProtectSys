cmake_minimum_required(VERSION 3.5)
project(FaceTracker)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")

find_package(OpenCV REQUIRED)

add_definitions(-mavx)
message(STATUS "Enabling AVX instructions")

set(SOURCE_FILES facetracker.cpp)
add_executable(FaceTracker ${SOURCE_FILES})

include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(FaceTracker ${OpenCV_LIBS})