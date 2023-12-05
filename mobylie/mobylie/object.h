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
	double x;
	double y;
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
	void updateVel(vec vel);
	void updateAcc(vec acc);
	void updatePos(vec pos);
	data getObjectData();


	void update(object& rhs);

	double calcIOU(object& rhs);
	vec getNewVec(vec newState, vec oldState,int new_time);


	
private:
	clock_t _lastCheck;
	data _objectData;
	std::string _name;
	int _imgData[4];
};
