# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/skywalker/Desktop/Dev/clion-2017.1/bin/cmake/bin/cmake

# The command to remove a file.
RM = /home/skywalker/Desktop/Dev/clion-2017.1/bin/cmake/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/FaceTracker.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/FaceTracker.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/FaceTracker.dir/flags.make

CMakeFiles/FaceTracker.dir/facetracker.cpp.o: CMakeFiles/FaceTracker.dir/flags.make
CMakeFiles/FaceTracker.dir/facetracker.cpp.o: ../facetracker.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/FaceTracker.dir/facetracker.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/FaceTracker.dir/facetracker.cpp.o -c "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/facetracker.cpp"

CMakeFiles/FaceTracker.dir/facetracker.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/FaceTracker.dir/facetracker.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/facetracker.cpp" > CMakeFiles/FaceTracker.dir/facetracker.cpp.i

CMakeFiles/FaceTracker.dir/facetracker.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/FaceTracker.dir/facetracker.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/facetracker.cpp" -o CMakeFiles/FaceTracker.dir/facetracker.cpp.s

CMakeFiles/FaceTracker.dir/facetracker.cpp.o.requires:

.PHONY : CMakeFiles/FaceTracker.dir/facetracker.cpp.o.requires

CMakeFiles/FaceTracker.dir/facetracker.cpp.o.provides: CMakeFiles/FaceTracker.dir/facetracker.cpp.o.requires
	$(MAKE) -f CMakeFiles/FaceTracker.dir/build.make CMakeFiles/FaceTracker.dir/facetracker.cpp.o.provides.build
.PHONY : CMakeFiles/FaceTracker.dir/facetracker.cpp.o.provides

CMakeFiles/FaceTracker.dir/facetracker.cpp.o.provides.build: CMakeFiles/FaceTracker.dir/facetracker.cpp.o


# Object files for target FaceTracker
FaceTracker_OBJECTS = \
"CMakeFiles/FaceTracker.dir/facetracker.cpp.o"

# External object files for target FaceTracker
FaceTracker_EXTERNAL_OBJECTS =

../FaceTracker: CMakeFiles/FaceTracker.dir/facetracker.cpp.o
../FaceTracker: CMakeFiles/FaceTracker.dir/build.make
../FaceTracker: /usr/local/lib/libopencv_stitching.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_superres.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_videostab.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_aruco.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_bgsegm.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_bioinspired.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_ccalib.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_dpm.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_freetype.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_fuzzy.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_line_descriptor.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_optflow.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_reg.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_saliency.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_stereo.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_structured_light.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_surface_matching.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_tracking.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_xfeatures2d.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_ximgproc.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_xobjdetect.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_xphoto.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_shape.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_phase_unwrapping.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_rgbd.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_calib3d.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_video.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_datasets.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_dnn.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_face.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_plot.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_text.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_features2d.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_flann.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_objdetect.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_ml.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_highgui.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_photo.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_videoio.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_imgcodecs.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_imgproc.so.3.2.0
../FaceTracker: /usr/local/lib/libopencv_core.so.3.2.0
../FaceTracker: CMakeFiles/FaceTracker.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../FaceTracker"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/FaceTracker.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/FaceTracker.dir/build: ../FaceTracker

.PHONY : CMakeFiles/FaceTracker.dir/build

CMakeFiles/FaceTracker.dir/requires: CMakeFiles/FaceTracker.dir/facetracker.cpp.o.requires

.PHONY : CMakeFiles/FaceTracker.dir/requires

CMakeFiles/FaceTracker.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/FaceTracker.dir/cmake_clean.cmake
.PHONY : CMakeFiles/FaceTracker.dir/clean

CMakeFiles/FaceTracker.dir/depend:
	cd "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera" "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera" "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug" "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug" "/home/skywalker/Desktop/Faks/Rektorova/Rad/Source Code/FaceRecProtectSys/ATMInterface/Camera/cmake-build-debug/CMakeFiles/FaceTracker.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/FaceTracker.dir/depend

