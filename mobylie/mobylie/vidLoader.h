#pragma once
#pragma once
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>

class vidLoader
{
public:
	const std::string frameFileName = "tempFile.png";
	vidLoader();//in live settings
	vidLoader(std::string path);//from a vid
	cv::Mat getNextFrame();
	cv::Mat getCurrentFrame();
private:
	cv::VideoCapture cap;
	cv::Mat Currntframe;
};


