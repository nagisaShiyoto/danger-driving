#pragma once
#include <iostream>
enum DATA
{
	X = 0,
	Y,
	WIDTH,
	HIGHT	
};
class vec
{
public:
	double x;
	double y;
	vec& operator+=(vec const& rhs);
	vec operator/(int const& rhs) const;
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
	static data getZeroData();
	object(const int imgData[],std::string name);
	object();
	void changeImgData(const int imgData[]);
	int* getDataImg();
	std::string getName()const;
	void updateVel(vec vel);
	void updateAcc(vec acc);
	void updatePos(vec pos);
	data getObjectData();
	vec getDistance();

	void update(object& rhs);

	double calcIOU(object& rhs);
	vec getNewVec(vec newState, vec oldState,int new_time);
	static vec calculate_distance_from_object(object& a, int angle1, object& b, int angle2, vec velocity);

	
private:
	clock_t _lastCheck;
	data _objectData;
	vec _distnacedMade;
	std::string _name;
	int _imgData[4];
};
