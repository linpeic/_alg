#include<stdio.h>
#include <stdlib.h>
#include <time.h>
#include <windows.h>

int people=0,wolf=1,sheep=3,veget=1,score=0;
int wolf_st=0,sheep_st=0,veget_st=0;

int main(){
    SetConsoleOutputCP(CP_UTF8);
    srand(time(NULL));
    if(wolf>sheep && veget<wolf){
        score=wolf;
        printf("第一次：狼先過，對面有：狼");
        printf("(分數%d)\n",score);
        wolf_st=1;
    }
    else if(sheep>wolf && sheep>veget){
        score=sheep;
        printf("第一次：羊先過，對面有：羊");
        printf("(分數%d)\n",score);
        sheep_st=1;
    }
    else{
        score=veget;
        printf("第一次：菜先過，對面有：菜");
        printf("(分數%d)\n",score);
        veget_st=1;
    }

    if(score+wolf==4 && score+veget==4){
        int choice = rand() % 2;
        //printf("選擇%d",choice);
        if(choice == 0) {
            score = wolf;
            printf("第二次：載狼過去，再載羊回去，對面有：狼");
            wolf_st=1;
            sheep_st=0;
            veget_st=0;
        } else {
            score = veget;
            printf("第二次：載菜過去，再載羊回去，對面有：菜");
            veget_st=1;
            sheep_st=0;
            wolf_st=0;
        }
        printf("(分數%d)\n",score);
    }

    if(wolf_st==0 &&veget_st==1 &&sheep_st==0){
        score=score+wolf;
        if(score<4){
            wolf_st=1;
            printf("第三次：狼過去，對面有：菜跟狼");
            printf("(分數%d)\n",score);
        }
    }
    else if(veget_st==0 &&sheep_st==0 && wolf_st==1){
        score=score+veget;
        if(score<4 ){
            veget_st=1;
            printf("第三次：載菜過去，對面有：狼跟菜");
            printf("(分數%d)\n",score);
        }
    }
    else if(sheep_st==0 && wolf_st==0 &&veget_st==1){
        score=score+sheep;
        if(score<4){
            sheep_st=1;
            printf("第三次：載羊過去，對面有：菜跟羊");
            printf("(分數%d)\n",score);
        }
    }
    else if(sheep_st==0 && veget_st==0 && wolf_st==1){
        score=score+sheep;
        if(score<4){
            sheep_st=1;
            printf("第三次：載羊過去，對面有：菜跟羊");
            printf("(分數%d)\n",score);
        }
    }
    if(wolf_st==1 &&veget_st==1 &&sheep_st==0){
        sheep_st=1;
        score=score+sheep;
        printf("第四次：羊過去，狼、羊、菜都在對面");
        printf("(分數%d)\n",score);
    }
    if(wolf_st==1 &&veget_st==1 &&sheep_st==1){
        printf("運送結束");
    }
}
