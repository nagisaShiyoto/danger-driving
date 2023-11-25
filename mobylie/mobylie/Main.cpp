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
            std::cout
                <<"\n\n\n"
                <<detector.dettectSign(loader.frameFileName) 
                <<"\n\n\n" 
                << detector.dettectCar(loader.frameFileName)
                ;
            time(&end);

            std::cout
                << "time:"
                << end - start
                <<"\n\n\n\n\n";

            if (cv::waitKey(1) >= 0)
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
