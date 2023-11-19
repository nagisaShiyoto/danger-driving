#include "vidLoader.h"

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
	this->cap >> this->Currntframe;
	return this->Currntframe;
}

cv::Mat vidLoader::getCurrentFrame()
{
	return this->Currntframe;
}
