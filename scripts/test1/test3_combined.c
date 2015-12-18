#include <klee/klee.h>
int func(){
  int x;
  int y;
  int z;
  int a;
  int b;
  int c;
  klee_make_symbolic(&x, sizeof x , "x");
  klee_make_symbolic(&y, sizeof y , "y");
  klee_make_symbolic(&z, sizeof z , "z");
  klee_make_symbolic(&a, sizeof a , "a");
  klee_make_symbolic(&b, sizeof b , "b");
  klee_make_symbolic(&c, sizeof c , "c");
  if(x == 0){
    y = y+1;
  }else if (x == 1) {
    y = y+2;
  } else{
    x=y;
  }
  if(true) {
    assert(true);
  }
  if(a==0){
    b =1;
  }else if(a==1){
    b =2;
  }
  if(y==2){
    z=0;
  }else if( y == 3){
    z=1;
  }else {
    z=2;
  }
  return 0;
}
int func_2(){
  int x;
  int y;
  int z;
  int a;
  int b;
  int c;
  klee_make_symbolic(&c, sizeof c , "x");
  klee_make_symbolic(&x, sizeof x , "x");
  klee_make_symbolic(&y, sizeof y , "y");
  klee_make_symbolic(&z, sizeof z , "z");
  klee_make_symbolic(&a, sizeof a , "a");
  klee_make_symbolic(&b, sizeof b , "b");
  if(x == 0){
    y = y+1;
  }else if (x == 1) {
    y = y+2;
  } else{
    x=y;
  }
  if(c > 5) {
    x = z + 1;
  }
  if(a==0){
    b =1;
  }else if(a==1){
    b =2;
  }
  if(y==2){
    z=0;
  }else if( y == 3){
    z=1;
  }else {
    z=2;
  }
  return 0;
}
int main(int argc, char** argv){
int g = func_2();return g;
}
