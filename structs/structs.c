#include <stdio.h>

struct point {
    int x;
    int y;
};

struct  point makepoint(int x, int y) {

    struct point temp;

    temp.x = x;
    temp.y = y;

    return temp;
}

int main() {

    struct point pt = makepoint(3,2);
    printf("point x=%d y=%d\n", pt.x, pt.y );

}