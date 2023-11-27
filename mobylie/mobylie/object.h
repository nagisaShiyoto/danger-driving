#pragma once
#include <iostream>
enum DATA
{
	X = 0,
	Y,
	WIDTH,
	LENGTH	
};
class object
{
public:
	object(const int imgData[],std::string name);
	void changeImgData(const int imgData[]);
	int* getDataImg();
	std::string getName()const;
	object& operator=(const object& rhs);

private:
	std::string _name;
	int _imgData[];
};

