#include "object.h"
#include <cmath>

int object::id = 0;
data object::getZeroData()
{
    data temp;
    vec zeroVec;
    zeroVec.x = 0;
    zeroVec.y = 0;
    temp.aceloration = zeroVec;
    temp.velocity = zeroVec;
    temp.position = zeroVec;
    return temp;
}
object::object(const int imgData[],std::string name)
{
    vec zeroVec;
    zeroVec.x = 0;
    zeroVec.y = 0;
	this->changeImgData(imgData);
	this->_name = name;
    this->_lastCheck = clock();
    this->_objectData = object::getZeroData();
    this->_distnacedMade = zeroVec;
    object::id++;
    ///////////////////////////test//////////////////////////////////
    this->_objectData.position.x = object::id * 2;
    this->_objectData.position.y = object::id * 2 + 1;
    ///////////////////////////test//////////////////////////////////

}
object::object()
{
    int img_data[] = { 0, 0, 0, 0 };
    object(img_data, "ourCar");
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
    return iou;
}

vec object::getNewVec(vec newState, vec oldState,int new_time)
{
    vec vel;
    double dt = (new_time - this->_lastCheck)/double(CLOCKS_PER_SEC);
    vel.x = double(newState.x - oldState.x) / dt;
    vel.y = double(newState.y - oldState.y) / dt;
    return vel;
}

/*
the function calcualtes the distance from a object


*/
vec object::calculate_distance_from_object(object& a, int angle1, object& b, int angle2, vec velocity)
{
    double m1 = tan(angle1);
    double m2 = tan(angle2); // Error on this line: you should subtract the Direction but I coudn't find where this os stored

    //Using the point - slope form : y - y1 = m1(x - x1) and y - y2 = m2(x - x2)
    //Rearranging these equations to the form of y = mx + c
    double c1 = a.getDistance().y - m1 * a.getDistance().x;
    double c2 = b.getDistance().y - m2 * b.getDistance().x;

    //Solving the two linear equations
    //y = m1 * x + c1 and y = m2 * x + c2    
    //m1 * x + c1 = m2 * x + c2 = > x = (c2 - c1) / (m1 - m2)
    double x3 = (c2 - c1) / (m1 - m2);
    double y3 = m1 * x3 + c1;
    
    return vec();
}

void object::updateVel(vec vel)
{
    this->_objectData.velocity = vel;
}

void object::updateAcc(vec acc)
{
    this->_objectData.aceloration = acc;
}

void object::updatePos(vec pos)
{
    this->_objectData.position.x = pos.x;
    this->_objectData.position.y = pos.y;
}

data object::getObjectData()
{
    return this->_objectData;
}

vec object::getDistance()
{
    return this->_distnacedMade;
}

void object::update(object& rhs)
//put rhs in this
//this-the new object
//rhs -the old object 
{
    clock_t newT = clock();
    this->_name = rhs.getName();

    this->_distnacedMade.x = this->_objectData.position.x - rhs.getObjectData().position.x;
    this->_distnacedMade.y = this->_objectData.position.y - rhs.getObjectData().position.y;
    //check if position exist
    if (rhs.getObjectData().position.x != 0 || rhs.getObjectData().position.y != 0)
    {
        vec vel = rhs.getNewVec(this->getObjectData().position,rhs.getObjectData().position, newT);
        if (rhs.getObjectData().velocity.x != 0 || rhs.getObjectData().velocity.y != 0)//if he has vel we can calc the acc
        {
            this->updateAcc(rhs.getNewVec(vel,rhs.getObjectData().velocity,newT));
        }
        this->updateVel(vel);
    }
    ///////////////////////////test//////////////////////////////////
    std::cout
        << "\n" << "---------------------------------" << this->_name << "--------------------------------"
        << "\n" << this->_distnacedMade.x << " " << this->_distnacedMade.y
        << "\n" << this->_objectData.position.x << " " << this->_objectData.position.y << " " << rhs.getObjectData().position.x << " " << rhs.getObjectData().position.y
        << "\n" << this->_objectData.velocity.x << " " << this->_objectData.velocity.y << " " << rhs.getObjectData().velocity.x << " " << rhs.getObjectData().velocity.y
        << "\n" << this->_objectData.aceloration.x << " " << this->_objectData.aceloration.y << " " << rhs.getObjectData().aceloration.x << " " << rhs.getObjectData().aceloration.y
        ;
    ///////////////////////////test//////////////////////////////////

    newT = clock();
    this->_lastCheck = newT;//update the time
}

vec& vec::operator+=(vec const& rhs)
{
    this->x += rhs.x;
    this->y += rhs.y;
    return *this;
}

vec vec::operator/(int const& rhs) const
{
    vec temp;
    temp.x = this->x / rhs;
    temp.y = this->y / rhs;
    return temp;
}
