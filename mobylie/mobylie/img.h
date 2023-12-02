#pragma once
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>

class img
{
public:
	//img();
	//img(cv::Mat img);
	void changeImg(cv::Mat img);
	cv::Mat getBgrImg();
	cv::Mat getHslImg();
	void printValues();
private:
	cv::Mat bgrImg;
	cv::Mat hslImg;
};

