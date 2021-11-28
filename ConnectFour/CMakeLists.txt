cmake_minimum_required(VERSION 3.20)
project(ConnectFour)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(ConnectFour
        game.cpp
        game.h
        main.cpp)
