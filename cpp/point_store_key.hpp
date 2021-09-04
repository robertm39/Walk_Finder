#pragma once

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

//very verboten - adding to std
namespace std
{
    struct hash<PointStoreKey>
    {
        size_t operator()(const PointStoreKey &k)
        {
            return (k.x() << 32) ^ k.y(); //This should be pretty good
        }
    };
};

const PointStoreKey operator+(const PointStoreKey&, const PointStoreKey&);

bool operator==(const PointStoreKey&, const PointStoreKey&);
