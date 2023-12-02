#include "vidLoader.h"
#include <iostream>

vidLoader::vidLoader()
{
	this->cap.open(0);//get feed from the first camera in setup
	if (!this->cap.isOpened())
	{
		throw std::exception("there isnt any camera found");//mybe make a real class exeption
	}
}

vidLoader::vidLoader(std::string path)
{
	if (path.empty())
	{
		this->cap.open(0);
	}
	else
	{
		this->cap.open(path);
	}
	if (!this->cap.isOpened())
	{
		throw std::exception("coudn't open file");
	}
}

cv::Mat vidLoader::getNextFrame()
{
	cv::Mat tempImg;
	this->cap >> tempImg;
	this->Currntframe.changeImg(tempImg);
	cv::imwrite(this->frameFileName, this->Currntframe.getBgrImg());//save img in file temp	;
	return this->Currntframe.getBgrImg();
}

img vidLoader::getCurrentFrame()
{
	return this->Currntframe;
}

