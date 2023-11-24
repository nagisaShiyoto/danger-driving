#pragma once
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/numpy.h>
namespace py = pybind11;
class imgDetector
{
public:
	imgDetector();
	std::string dettectSign(std::string imgName);
	std::string dettectCar(std::string imgName);
private:
	pybind11::scoped_interpreter* _interpreter2;
	pybind11::object signDFanc;
	pybind11::object carDFanc;
};

