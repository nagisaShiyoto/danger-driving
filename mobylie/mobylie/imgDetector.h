#pragma once
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
#include "object.h"
#include "Vehicle.h"
#include "Sign.h"
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
	void updateOurCar();
	object getOurCar();
	std::vector<object*> foundVehicles;
	std::vector<object*> foundSigns;


private:
	object _ourCar;
	void compareVectors(std::vector<object*> temp,bool carVector);
	std::vector<std::string> split(std::string str, std::string delim);
	pybind11::scoped_interpreter* _interpreter2;
	pybind11::object signDFanc;
	pybind11::object carDFanc;
};

