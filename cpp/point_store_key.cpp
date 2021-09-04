#include "point_store_key.hpp"

const PointStoreKey operator+(const PointStoreKey &k1, const PointStoreKey &k2)
{
    return PointStoreKey(k1.x() + k2.x(), k1.y() + k2.y());
}

bool operator==(const PointStoreKey &k1, const PointStoreKey &k2)
{
    return k1.x() == k2.x() && k2.y() == k2.y();
}