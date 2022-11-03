#include"iostream"
#include<stdio.h>
#include <time.h>
#include<windows.h>
#include<stdlib.h>
#include<conio.h>
//#include"graphic.h"
using namespace std;
void record();
void gotoxy(int x, int y);
bool gameOver;
const int width=20;
const int height=20;
int x,y;
int fruitX,fruitY,score;
enum eDirecton{STOP=0,LEFT,RIGHT,UP,DOWN};
eDirecton dir;
int nTail;
int tailX[100],tailY[100];

void start()
{
    cout<<endl<<endl<<endl;
    cout<<"                                    Start Game "<<endl<<endl<<endl<<endl;
    cout<<"                                 Press 1 to start  ";
}
void Setup()
{
    gameOver=false;
    dir=STOP;
    x=width/2;
    y=width/2;
    //y1=(width/2)+1;
    fruitX=rand()%width;
    fruitY=rand()%height;
    score=0;
}

void Draw()
{
    system("cls");
    for(int i=0;i<width+2;i++)
        cout<<"=";
        cout<<endl;


    for(int i=0;i<height;i++)
    {
        for(int j=0;j<width;j++)
        {
           if(j==0)
                cout<<"|";
               if(i==y && j==x)
                    cout<<"0";
                else if(i==fruitY && j==fruitX)
                    cout<<"F";
            else
                {
                   bool print=false;
                   for(int k=0;k<nTail;k++)
                   {
                       if(tailX[k]==j && tailY[k]==i)
                       {
                           cout<<"o";
                           print=true;
                       }
                   }
                   if(!print)
                    cout<<" ";
                }

            if(j==width-1)
                cout<<"|";

        }
        cout<<endl;
    }


    for(int i=0;i<width+2;i++)
        cout<<"=";
        cout<<endl;

    cout<<"Score :"<<score<<endl;
    cout <<" Game Over ";
}

void Input()
{
    if(_kbhit())
    {
        switch(_getch())
        {
        case 'a':
            dir=LEFT;
            break;
        case 'd':
            dir=RIGHT;
            break;
        case 'w':
            dir=UP;
            break;
        case 's':
            dir=DOWN;
            break;
        case 'x':
            gameOver=true;
            break;
        }
    }
}

void Logic()
{
    int prevX=tailX[0];
    int prevY=tailY[0];
    int prev2X,prev2Y;
    tailX[0]=x;
    tailY[0]=y;

    for(int i=1;i<nTail;i++)
    {
        prev2X=tailX[i];
        prev2Y=tailY[i];
        tailX[i]=prevX;
        tailY[i]=prevY;
        prevX=prev2X;
        prevY=prev2Y;

    }
    switch(dir)
    {
        case LEFT:
            x--;
            break;
        case RIGHT:
            x++;
            break;
        case UP:
            y--;
            break;
        case DOWN:
            y++;
            break;
        default:
            break;
    }

    //if(x>width || x<0 || y>height || y<0)   //Game over if hit the wall.
    //gameOver=true;

   if(x>=width) x=0;else if(x<0)x=width-1;  //Game will not over by hit the wall
   if(y>=height) y=0;else if(y<0)y=height-1;

     for(int i=0;i<nTail;i++){
           if(tailX[i]==x && tailY[i]==y)   //self loop cut.
           gameOver=true;
           //cout<<"tail:"<<tailX[i]<<"  "<<tailY[i]<<" "<<endl;
           //cout<<"XY"<<x<<"  "<<y<<" ";

     }

    if(x==fruitX && y==fruitY)
    {
        score+=10;
        fruitX=rand()%width;
        fruitY=rand()%height;
        nTail++;
    }
}

void Score()
{
    cout<<score;
}

void load(){
    int row,col,r,c,q;
    gotoxy(36,14);
    printf("loading...");
    gotoxy(30,15);
    for(r=1;r<=20;r++){
    Sleep(200);//to display the character slowly
    printf("%c",177);}
    //getch();
}
void gotoxy(int x, int y)
{

 COORD coord;

 coord.X = x;

 coord.Y = y;

 SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);

}

void record(){
   char plname[20],nplname[20],cha,c;
   int i,j,px;
   FILE *info;
   info=fopen("record.txt","a+");
   getch();
   system("cls");
   printf("Enter your name\n");
   //scanf("%[^\n]",plname);
   scanf("%s",plname);
   //************************
   for(j=0;plname[j]!='\0';j++){ //to convert the first letter after space to capital
   nplname[0]=toupper(plname[0]);
   if(plname[j-1]==' '){
   nplname[j]=toupper(plname[j]);
   nplname[j-1]=plname[j-1];}
   else nplname[j]=plname[j];
   }
   nplname[j]='\0';
   //*****************************
   //sdfprintf(info,"\t\t\tPlayers List\n");
   fprintf(info,"Player Name :%s\n",nplname);


   time_t mytime;       //for date and time
  mytime = time(NULL);
  fprintf(info,"Played Date:%s",ctime(&mytime));
     //**************************
     fprintf(info,"Score:%d\n",px=score);//call score to display score
     //fprintf(info,"\nLevel:%d\n",10);//call level to display level
   for(i=0;i<=50;i++)
   fprintf(info,"%c",'_');
   fprintf(info,"\n");
   fclose(info);
   printf("wanna see past records press 'y'\n");
   cha=getch();
   system("cls");
   if(cha=='y'){
   info=fopen("record.txt","r");
   do{
       putchar(c=getc(info));
       }while(c!=EOF);}
     fclose(info);
}
main()
{
    Setup();
    start();
    int n;
    cin>>n;
    if(n==1)
        load();
    {
        while(!gameOver)
        {
            Draw();
            Input();
            Logic();
            Sleep(100);
        }
    }
    record();
}
