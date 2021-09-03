#include <iostream>
#include <cmath>

#include <boost/multiprecision/cpp_bin_float.hpp>
#include <boost/multiprecision/number.hpp>

using std::cout;
using std::endl;
using std::sqrt;

using boost::multiprecision::cpp_bin_float_oct;
using boost::multiprecision::cpp_bin_float;
using boost::multiprecision::number;

typedef cpp_bin_float_oct oct;
typedef number<cpp_bin_float<105> > float_105;

//And here is the one I actually use
typedef float_105 b_float;

//So this seems to actually work
//I get the promised precision

// It worked for taking the square root of two
// How do they even make it work with the standard library functions

int main()
{
    //b_float ten = 10;
    //b_float ten_power_ten = 

    /*b_float one = 1;
    b_float three = 3;
    b_float precise_third = one / three;
    cout.precision(110);
    cout << "Precise Third: " << precise_third << endl;*/
    cout.precision(110);
    b_float two = 2;
    b_float sqrt_2 = sqrt(two);
    cout << "Sqrt(2): " << sqrt_2 << endl;
    cout << "squared: " << sqrt_2 * sqrt_2 << endl;

    return 0;
}