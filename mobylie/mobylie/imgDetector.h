#pragma once
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
#include "object.h"
#include <vector>
namespace py = pybind11;
class imgDetector
{
public:
	imgDetector();
	std::string dettectSign(std::string imgName);
	std::string dettectCar(std::string imgName);
	void updateCars(std::string);
	void updateSigns(std::string);
	std::vector<object*> getFoundVehicles()const;
	std::vector<object*> getFoundSigns()const;
private:
	std::vector<std::string> split(std::string str, std::string delim);
	pybind11::scoped_interpreter* _interpreter2;
	pybind11::object signDFanc;
	pybind11::object carDFanc;
	std::vector<object*> foundVehicles;
	std::vector<object*> foundSigns;

};

