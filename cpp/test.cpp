#include <iostream>
#include <cmath>

#include "constants.hpp"
#include "point.hpp"

using std::cout;
using std::stringstream;
using std::endl;
using std::sqrt;

//using point::Point;

//code adapted from
//https://www.boost.org/doc/libs/1_77_0/libs/multiprecision/doc/html/boost_multiprecision/tut/input_output.html
bool check_roundtrip(b_float val)
{
    std::stringstream ss;  // Read and write std::stringstream.
    ss.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
    ss.flags(std::ios_base::fmtflags(std::ios_base::scientific)); // Use scientific format.

    ss << val;
    b_float read_val;
    ss >> read_val;
    return val == read_val;
}

void general_test()
{
    //b_float ten = 10;
    //b_float ten_power_ten = pow(ten, 100);
    //b_float eps = b_float(1) / ten_power_ten;
    cout << "Eps: " << EPS << endl;

    /*b_float one = 1;
    b_float three = 3;
    b_float precise_third = one / three;
    cout.precision(110);
    cout << "Precise Third: " << precise_third << endl;*/
    b_float two = 2;
    b_float sqrt_2 = sqrt(two);
    cout << "Sqrt(2): " << sqrt_2 << endl;
    cout << "squared: " << sqrt_2 * sqrt_2 << endl;
    cout << "Size of b_float: " << sizeof(two) << endl;

    cout << "Checking round trips:" << endl;
    cout << "Two: " << check_roundtrip(two) << endl;
    cout << "Sqrt(2): " << check_roundtrip(sqrt_2) << endl;
}

void point_test()
{
    Point p1(b_float(-0.5), b_float(1) / 3);
    cout << "x: " << p1.x() << endl;
    cout << "y: " << p1.y() << endl;
    cout << "p1: " << p1 << endl;

    Point p2(5, 1);
    cout << "p2: " << p2 << endl;
    cout << "p1 + p2: " << p1 + p2 << endl;
    cout << "len of p2: " << p2.norm() << endl;
}

int main()
{
    cout.precision(std::numeric_limits<b_float>::max_digits10);  // Ensure all potentially significant bits are output.
    cout.flags(std::ios_base::fmtflags(std::ios_base::scientific)); // Use scientific format.

    point_test();

    return 0;
}