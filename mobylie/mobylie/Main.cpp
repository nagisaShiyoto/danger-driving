//////////////////general includes//////////////////
#include <iostream>
//////////////////general includes//////////////////

//////////////////opencv includes////////////////////
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
using namespace cv;

//////////////////opencv includes////////////////////

//////////////////pybind includes////////////////////
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
namespace py = pybind11;

//////////////////pybind includes////////////////////

int main() {

    cv::Mat img = cv::imread("C:\\Users\\test0\\Downloads\\idkk\\input_images\\test.jpg");
    namedWindow("First OpenCV Application", WINDOW_AUTOSIZE);
    cv::imshow("First OpenCV Application", img);
    cv::moveWindow("First OpenCV Application", 0, 45);
    cv::waitKey(0);
    cv::destroyAllWindows();
    try
    {
        // Create a scoped interpreter for the second Python environment
        pybind11::scoped_interpreter interpreter2("/Scripts/python.exe");

        // Import the Python module from the second environment
        auto nul = py::module::import("detection_from_folder"); // import the sign module
        auto multipl = nul.attr("add"); // get fanc
        multipl("C:/Users/test0/Downloads/idkk/input_images"); // use

        auto test = py::module::import("detect");//import the car(and poeple) module
        auto testFanc = test.attr("run");//get fanc
        testFanc();//use
    }
    catch (const py::error_already_set& e) {
        std::cerr << "Python error: " << e.what() << std::endl;
    }
    return 0;
}
