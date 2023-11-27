#include "imgDetector.h"
#include <string.h>
imgDetector::imgDetector()
{
	// Create a scoped interpreter for the second Python environment
	this->_interpreter2 = new py::scoped_interpreter("/Scripts/python.exe");
	auto signDFile = py::module::import("SignDetection");
	this->signDFanc = signDFile.attr("run");
	auto carDFile = py::module::import("detect");
	this->carDFanc = carDFile.attr("run");
}

std::string imgDetector::dettectSign(std::string imgName)
{
	return this->signDFanc(imgName).cast<std::string>();
}

std::string imgDetector::dettectCar(std::string imgName)
{
	return this->carDFanc(imgName).cast<std::string>();
}

void imgDetector::updateCars(std::string res)
{
	const int OBJ = 4;
	if (res == "not found")
	{
		this->foundVehicles.clear();//no cars
	}
	else
	{
		this->foundVehicles.clear();//no cars
		std::vector<std::string> objects = this->split(res, "\n");
		std::vector<std::string> splited;
		int data[4];
		for (auto it = objects.begin(); it != objects.end()&&it->size() != 0; it++)
		{
			splited = this->split(*it, ",");
			for (int i = 0; i <= LENGTH; i++)
			{
				splited[i] = splited[i].substr(1, splited[i].find(".")-1);
				data[i] = std::stoi(splited[i]);
			}
			
			this->foundVehicles.push_back(new object(data,splited[OBJ]));
		}
	}
}

void imgDetector::updateSigns(std::string res)
{
	const int OBJ = 4;
	if (res == "not found")
	{
		this->foundSigns.clear();//no cars
	}
	else
	{
		this->foundSigns.clear();//no cars
		std::vector<std::string> objects = this->split(res, "\n");
		std::vector<std::string> splited;
		int data[4];
		for (auto it = objects.begin(); it != objects.end() && it->size() != 0; it++)
		{
			splited = this->split(*it, ",");
			for (int i = 0; i <= LENGTH; i++)
			{
				splited[i] = splited[i].substr(1, splited[i].find(".") - 1);
				data[i] = std::stoi(splited[i]);
			}

			this->foundSigns.push_back(new object(data, splited[OBJ]));
		}
	}
}

std::vector<object*> imgDetector::getFoundVehicles()const
{
	return this->foundVehicles;
}

std::vector<object*> imgDetector::getFoundSigns()const
{
	return this->foundSigns;
}

std::vector<std::string> imgDetector::split(std::string str, std::string delim)
{
	std::vector<std::string> splited;
	int start, end = -1 * delim.size();
	do {
		start = end + delim.size();
		end = str.find(delim, start);
		splited.push_back(str.substr(start, end - start));
	} while (end != -1);
	return splited;
}