#pragma once
#include <iostream>
enum DATA
{
	X = 0,
	Y,
	WIDTH,
	HIGHT	
};
struct vec
{
	int x;
	int y;
};
struct data
{
	struct vec position;
	struct vec velocity;
	struct vec aceloration;
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
	int _imgData[4];
};

