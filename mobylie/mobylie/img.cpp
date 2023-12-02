#include "img.h"

void img::changeImg(cv::Mat img)
{
	this->bgrImg = img;
	cv::cvtColor(this->bgrImg, this->hslImg, cv::COLOR_RGB2HLS);
}

cv::Mat img::getBgrImg()
{
	return this->bgrImg;
}

cv::Mat img::getHslImg()
{
	return this->hslImg;
}

void img::printValues()
{
	int const SAMPLE_TEST = 10;
	unsigned char* bgrPixels = (unsigned char*)this->bgrImg.data;

	unsigned char* hslPixels = (unsigned char*)this->hslImg.data;

	std::cout << "-------------------------bgr-----------------------------------";
	for (int row = 0; row < SAMPLE_TEST/*this->bgrImg.rows*/; row++)
	{
		for (int col = 0; col < SAMPLE_TEST/*col < this->bgrImg.cols*/; col++)
		{
			std::cout << static_cast<int>(bgrPixels[row * this->bgrImg.cols + col])
				<< "," << static_cast<int>(bgrPixels[row * this->bgrImg.cols + col + 1])
				<< "," << static_cast<int>(bgrPixels[row * this->bgrImg.cols + col + 2])
					<<" ";
		}
		std::cout << std::endl;
	}

	std::cout << "-------------------------hsl-----------------------------------";
	for (int row = 0; row < SAMPLE_TEST /*this->hslImg.rows*/; row++)
	{
		for (int col = 0; col < SAMPLE_TEST /* this->hslImg.cols*/; col++)
		{
			std::cout << static_cast<int>(hslPixels[row * this->hslImg.cols + col])
				<< "," << static_cast<int>(hslPixels[row * this->hslImg.cols + col + 1])
				<< "," << static_cast<int>(hslPixels[row * this->hslImg.cols + col + 2])
				<< " ";
		}
		std::cout << std::endl;
	}
}
