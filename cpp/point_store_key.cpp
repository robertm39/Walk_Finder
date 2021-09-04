#include "point_store_key.hpp"


/*bool operator<(const PointStoreKey &k1, const PointStoreKey &k2)
{
    if(k1.x() < k2.x())
    {
        return true;
    }
    if(k1.x() > k2.x())
    {
        return false;
    }
    return k1.y() < k2.y();
}

bool operator<=(const PointStoreKey &k1, const PointStoreKey &k2);
bool operator>(const PointStoreKey &k1, const PointStoreKey &k2);
bool operator>=(const PointStoreKey &k1, const PointStoreKey &k2);*/
bool operator==(const PointStoreKey &k1, const PointStoreKey &k2)
{
    return k1.x() == k2.x() && k2.y() == k2.y();
}