#pragma once
#include <iostream>
enum DATA
{
	X = 0,
	Y,
	WIDTH,
	HIGHT	
};
class object
{
public:
	static int id;
	object(const int imgData[],std::string name);
	void changeImgData(const int imgData[]);
	int* getDataImg();
	std::string getName()const;
	void update(object& rhs);
	object& operator=(const object& rhs);
	double calcIOU(object& rhs);
private:
	std::string _name;
	int _imgData[];
};

