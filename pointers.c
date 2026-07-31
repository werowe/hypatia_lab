 #include <stdio.h>
 
 
int main() {
    


  int x = 1, y = 2, z[10];
   int *ip;          /* ip is a pointer to int */
   ip = &x;          /* ip now points to x */
   y = *ip;          /* y is now 1 */
   *ip = 0;          /* x is now 0 */
   ip = &z[0];       /* ip now points to z[0] */

// add
   *ip = *ip + 10;
// increments *ip by 10.

  printf("address of x %p\n", ip);

  // is usually a virtual memory address in your process, not a raw physical RAM address.
/* 
Your C program normally cannot discover or use the physical address directly. It does not need to: every load 
or store through &x is automatically translated by the hardware. 
Also, the address may change each time you run the program because of ASLR—address-space layout randomization:

The fact that addresses change between runs is specifically a security feature called ASLR—Address Space Layout 
Randomization. 
It makes it harder for an attacker to predict where the stack, libraries, and other data are located.

*/

/* &x = 0x16fb02fc0        virtual address visible to your program
          ↓
operating-system page-table translation
          ↓
physical RAM location

*/


// increments what ip points to, as do

  *ip += 1

/*

++*ip
and 
   (*ip)++
*/



}