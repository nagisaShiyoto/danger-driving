#include "object.h"

object::object(const int imgData[],std::string name)
{
	this->changeImgData(imgData);
	this->_name = name;
}

void object::changeImgData(const int imgData[])
{
	this->_imgData[X] = imgData[X];
	this->_imgData[Y] = imgData[Y];
	this->_imgData[WIDTH] = imgData[WIDTH];
	this->_imgData[LENGTH] = imgData[LENGTH];
}

int* object::getDataImg()
{
	return this->_imgData;
}

std::string object::getName() const
{
	return this->_name;
}

object& object::operator=(const object& rhs)
{
	//mybe adding check if they are the same name
	object temp(rhs._imgData, rhs.getName());
	return temp;
}