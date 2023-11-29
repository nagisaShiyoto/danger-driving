#include "object.h"
int object::id = 0;
object::object(const int imgData[],std::string name)
{
	this->changeImgData(imgData);
	this->_name = name;
    object::id++;

}

void object::changeImgData(const int imgData[])
{
	this->_imgData[X] = imgData[X];
	this->_imgData[Y] = imgData[Y];
	this->_imgData[WIDTH] = imgData[WIDTH];
	this->_imgData[HIGHT] = imgData[HIGHT];
}

int* object::getDataImg()
{
	return this->_imgData;
}

std::string object::getName() const
{
	return this->_name;
}

std::pair<int, int> getTopLeftPoint(object& rhs)
{
    std::pair<int, int> xy;
    xy.first = rhs.getDataImg()[X] - rhs.getDataImg()[WIDTH] / 2;
    xy.second = rhs.getDataImg()[Y] + rhs.getDataImg()[HIGHT] / 2;
    return xy;
}
double object::calcIOU(object& rhs)
{
    std::pair<int, int> xy1 = getTopLeftPoint(*this);
    std::pair<int, int> xy2 = getTopLeftPoint(rhs);
    // Calculate the (x, y) coordinates of the intersections
    int x_left = std::max(xy1.first, xy2.first);
    int y_top = std::min(xy1.second, xy2.second);
    int x_right = std::min(xy1.first + this->getDataImg()[WIDTH], xy2.first + rhs.getDataImg()[WIDTH]);
    int y_bottom = std::max(xy1.second - this->getDataImg()[HIGHT], xy2.second - rhs.getDataImg()[HIGHT]);

    // Calculate area of intersection
    int intersectionArea = std::max(0, std::abs(x_left-x_right)) * std::max(0, std::abs(y_top -y_bottom ));

    // Calculate area of both bounding boxes
    int box1Area = this->getDataImg()[WIDTH] * this->getDataImg()[HIGHT];
    int box2Area = rhs.getDataImg()[WIDTH] * rhs.getDataImg()[HIGHT];

    // Calculate union area
    int unionArea = box1Area + box2Area - intersectionArea;

    // Calculate IOU
    float iou = static_cast<float>(intersectionArea) / static_cast<float>(unionArea);
    //double iou =  intersectionArea/((box1Area + box2Area) / 2.0);
    return iou;
}

void object::update(object& rhs)
{
    this->_name = rhs.getName();
    //this->changeImgData( rhs.getDataImg());
}

object& object::operator=(const object& rhs)
{
	//mybe adding check if they are the same name
	object temp(rhs._imgData, rhs.getName());
	return temp;
}