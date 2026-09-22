#include <stdio.h>
#include <stdbool.h>
#include <strings.h>


const int TALL_LIMIT = 2;


bool is_tall(float height) {

   if (height >= TALL_LIMIT) {
    return true;
   }
    else {

        return false;
    }

}

bool and(bool left, bool right) {

  return left && right;

}

// homework

// or means left or right are true
bool or() {
    
}

// xor means left or right are true but not both
// true or true<---XOR is false

bool xor() {
    
}

// not and true and true is true.  this is only false when true and true
//  not and they write that because they are talking about AND   
// true AND true == true  , so we can also say not AND 
bool nand() {
    
}


int main()
{

    /* or

     and &&    
     or  ||
     not `
     xor
     nand

    */ 

    bool george = is_tall(2);  // we wrote is_tall to be true if height >= 2
    bool jeremy = is_tall(1.83);  // this means jeremy = false or 0
  

    printf("george %d\n", george);
    printf("jeremy %d\n", jeremy);

    //  here george is true and jeremy is false
    //  because above we wrote is_tall and we said that means true if > 2
    //  then we defined and to be george && jeremy
    printf("\n\nare george and jeremy tall %d", and(george,jeremy));
  

    return 0;
}
