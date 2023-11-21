//////////////////general includes//////////////////
#include <iostream>
#include "vidLoader.h"
//////////////////general includes//////////////////

//////////////////opencv includes////////////////////


//////////////////opencv includes////////////////////

//////////////////pybind includes////////////////////
#include <pybind11/embed.h>
#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
namespace py = pybind11;

//////////////////pybind includes////////////////////

int main() {
    std::string const VIDEO_NAME = "highway1.mp4";
    bool const LIVE = false;
    cv::namedWindow("test", cv::WINDOW_AUTOSIZE);
    cv::VideoCapture cap;
    vidLoader loader("videos/" + VIDEO_NAME);
    //vidLoader loader("");
    cv::Mat frame = loader.getNextFrame();
    while (!frame.empty())
    {

        cv::imshow("test", frame);
        if (cv::waitKey(1) >= 0)
        {
            break;
        }
        frame = loader.getNextFrame();
    }
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
        std::cerr << "Pythonn error: " << e.what() << std::endl;
    }
    return 0;
}
