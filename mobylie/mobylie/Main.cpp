//////////////////general includes//////////////////
#include <iostream>
#include "imgDetector.h"
#include "vidLoader.h"
//////////////////general includes//////////////////
#include <torch/torch.h>
#include <torch/script.h>
#include <opencv2/opencv.hpp>

int main() {
    // Load the image
    cv::Mat image = cv::imread("C:/Users/test0/OneDrive/שולחן העבודה/magshimim/eylon_yotam_project/mobylie/mobylie/tempFile.png");

    // Preprocess the image
    cv::resize(image, image, cv::Size(640, 640));
    cv::cvtColor(image, image, cv::COLOR_BGR2RGB);
    image.convertTo(image, CV_32FC3);

    // Normalize the image
    image /= 255.0;
    //image -= torch::tensor({ 0.485, 0.456, 0.406 });
    //image /= torch::tensor({ 0.229, 0.224, 0.225 });

    // Load the model
    try {
        torch::jit::Module model = torch::jit::load("C:/Users/test0/Downloads/idkk/yolov5cc.pt");
        // ...

        clock_t start, end;
        start = clock();//test
        torch::Tensor input = torch::from_blob(image.data, torch::IntList({ 1, 3, 640, 640 }), torch::kFloat32);

        torch::Tensor output = model.forward({input}).toTuple()->elements()[0].toTensor();
        end = clock();


        std::cout
            << "\n\n\n\n\n"
            << "time:"
            << double(end - start) / double(CLOCKS_PER_SEC)
            << "\n\n\n\n\n";
    }
    catch (const std::exception& e) {
        std::cerr << "Error loading model: " << e.what() << std::endl;
    }








    try
    {
        imgDetector detector;
        std::string const VIDEO_NAME = "highway1.mp4";
        bool const LIVE = false;
        cv::namedWindow("test", cv::WINDOW_AUTOSIZE);
        cv::namedWindow("test1", cv::WINDOW_AUTOSIZE);
        cv::VideoCapture cap;
        vidLoader loader("videos/" + VIDEO_NAME);
        //vidLoader loader("");
        cv::Mat frame = loader.getNextFrame();

        while (!frame.empty())
        {
            clock_t start, end;
            start = clock();//test
            std::string CarRes = detector.dettectCar(loader.frameFileName);
            std::string signRes = detector.dettectSign(loader.frameFileName);
            detector.updateCars(CarRes);
            detector.updateSigns(signRes);
            detector.updateOurCar();


            ////////////////////////////////////////////test/////////////////////////////////////////////////////////////////
            for (auto it = detector.foundVehicles.begin(); it != detector.foundVehicles.end(); it++)
            {
                int* data = (*it)->getDataImg();
                cv::Point topLeft(data[X] - data[WIDTH] / 2, data[Y] + data[HIGHT] / 2);
                cv::Point bottomRight(data[X] + data[WIDTH] / 2, data[Y] - data[HIGHT] / 2);
                cv::Rect rectangle(topLeft, bottomRight);
                cv::rectangle(frame, rectangle, cv::Scalar(255, 0, 0), 1);
                std::string text = (* it)->getName();
                cv::Point textPosition(topLeft.x, topLeft.y + 10);

                cv::putText(frame, text, textPosition, cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 0, 0), 2);

            }

            ///////////////////////////test//////////////////////////////////
            std::cout
                << "\n" << "---------------------------------" << "ourCar" << "--------------------------------"
                << "\n" << detector.getOurCar().getObjectData().position.x << " " << detector.getOurCar().getObjectData().position.y
                << "\n" << detector.getOurCar().getObjectData().velocity.x << " " << detector.getOurCar().getObjectData().velocity.y
                << "\n" << detector.getOurCar().getObjectData().aceloration.x << " " << detector.getOurCar().getObjectData().aceloration.y
                ;
            ///////////////////////////test//////////////////////////////////
            
            end=clock();
            

            std::cout
                <<"\n\n\n\n\n"
                << "time:"
                << double(end - start)/double(CLOCKS_PER_SEC)
                <<"\n\n\n\n\n";

            if (cv::waitKey(30) >= 0)
            {
                break;
            }
            cv::imshow("test", frame);

            frame = loader.getNextFrame();
            loader.getCurrentFrame().printValues();
            cv::imshow("test1", loader.getCurrentFrame().getHslImg());
            ////////////////////////////////////////////test/////////////////////////////////////////////////////////////////
        }
    }
    catch (const py::error_already_set& e) {
        std::cerr << "Pythonn error: " << e.what() << std::endl;
    }
    catch (const std::exception& e) {
        std::cerr << "Error loading model: " << e.what() << std::endl;
    }
    

    cv::destroyAllWindows();
    return 0;
}
