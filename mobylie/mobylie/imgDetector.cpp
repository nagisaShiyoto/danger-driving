#include "imgDetector.h"

imgDetector::imgDetector()
{
	// Create a scoped interpreter for the second Python environment
	this->_interpreter2 = new py::scoped_interpreter("/Scripts/python.exe");
	//auto signDFile = py::module::import("detection_from_folder");
	//this->signDFanc = signDFile.attr("add");
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
