//////////////////general includes//////////////////
#include <iostream>
#include "imgDetector.h"
#include "vidLoader.h"
//////////////////general includes//////////////////


int main() {
    try
    {
        imgDetector detector;
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
            time_t start, end;
            time(&start);
            std::string CarRes = detector.dettectCar(loader.frameFileName);
            std::string signRes = detector.dettectSign(loader.frameFileName);
            detector.updateCars(CarRes);
            detector.updateSigns(signRes);
            std::cout<<detector.getFoundVehicles()[0]->getName();
            time(&end);
            
            std::cout
                <<"\n\n\n\n\n"
                << "time:"
                << end - start
                <<"\n\n\n\n\n";

            if (cv::waitKey(30) >= 0)
            {
                break;
            }
            frame = loader.getNextFrame();
        }
    }
    catch (const py::error_already_set& e) {
        std::cerr << "Pythonn error: " << e.what() << std::endl;
    }
    cv::destroyAllWindows();
    return 0;
}
