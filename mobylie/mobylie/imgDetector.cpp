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
		std::vector<object*> temp;
		std::vector<std::string> objects = this->split(res, "\n");
		std::vector<std::string> splited;
		int data[4];
		for (auto it = objects.begin(); it != objects.end()&&it->size() != 0; it++)
		{
			splited = this->split(*it, ",");
			for (int i = 0; i <= HIGHT; i++)
			{
				splited[i] = splited[i].substr(1, splited[i].find(".")-1);
				data[i] = std::stoi(splited[i]);
			}
			
			temp.push_back(new object(data,splited[OBJ]+std::to_string(object::id)));
		}
		if (this->foundVehicles.size() > 0)
		{
			this->compareVectors(temp, true);
		}
		else
		{
			this->foundVehicles = temp;
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
		std::vector<object*> temp;
		std::vector<std::string> objects = this->split(res, "\n");
		std::vector<std::string> splited;
		int data[4];
		for (auto it = objects.begin(); it != objects.end() && it->size() != 0; it++)
		{
			splited = this->split(*it, ",");
			for (int i = 0; i <= HIGHT; i++)
			{
				splited[i] = splited[i].substr(1, splited[i].find(".") - 1);
				data[i] = std::stoi(splited[i]);
			}

			temp.push_back(new object(data, splited[OBJ]));
		}
		if (this->foundSigns.size() > 0)
		{
			this->compareVectors(temp, false);
		}
		else
		{
			this->foundSigns = temp;
		}
	}
}

void imgDetector::compareVectors(std::vector<object*> temp,bool carVector)
{
	const double IUO_THRESHOLD = 0.5;
	for (auto it = temp.begin(); it != temp.end(); it++)
	{
		//std::pair<double ,object*>bigIOU;
		//bigIOU.first = 0;
		for (auto j = this->foundVehicles.begin(); j != this->foundVehicles.end() && carVector; j++)
		{
			double iou= (*it)->calcIOU(**j);
			if ((*it)->getName().substr(0,1) == (*j)->getName().substr(0,1) && iou >= IUO_THRESHOLD)
			{
				(*it)->update(**j);//put it
				this->foundVehicles.erase(j);
				break;
			}
		}
		

		for (auto j = this->foundSigns.begin(); j != this->foundSigns.end() && !carVector; j++)
		{
			if ((*it)->getName() == (*j)->getName() && (*it)->calcIOU(**j) >= IUO_THRESHOLD)
			{
				(*it)->update(**j);//put it
				break;
			}
		}
	}
	if (carVector)
	{
		this->foundVehicles = temp;
	}
	else
	{
		this->foundSigns = temp;
	}

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