#pragma once
#include "img.h"

class vidLoader
{
public:
	const std::string frameFileName = "tempFile.png";
	vidLoader();//in live settings
	vidLoader(std::string path);//from a vid
	cv::Mat getNextFrame();
	img getCurrentFrame();
private:
	cv::VideoCapture cap;
	img Currntframe;
	//cv::Mat Currntframe;
};


