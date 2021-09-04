#pragma once

//using std::size_t;

//These won't actually be used as keys now
//because I'm using ints
class PointStoreKey
{
    private:
        const int x_;
        const int y_;
    public:
        int x() const {return x_;}
        int y() const {return y_;}
        PointStoreKey(int x, int y): x_(x), y_(y) {}
};
/*
//very verboten - adding to std
namespace std
{
    template <>
    struct hash<PointStoreKey>
    {
        size_t operator()(const PointStoreKey &k)
        {
            size_t t_x = k.x();
            size_t t_y = k.y();
            return (t_x << 32) ^ t_y; //This should be pretty good
        }
    };
};
*/
const PointStoreKey operator+(const PointStoreKey&, const PointStoreKey&);

bool operator==(const PointStoreKey&, const PointStoreKey&);
