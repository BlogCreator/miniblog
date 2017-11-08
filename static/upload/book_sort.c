#include <stdio.h>
#include <string.h>
struct stu{
  char name[21];
  int score;
};
int main()
{
    int n,m;
    char f[21];
    scanf("%d",&n);
    struct stu book[101],t;
    for(int i=0;i<101;i++)
    {
      book[i].score=0;
    }
    for(int i=0;i<n;i++)
    {
      scanf("%s %d",f,&m);
      book[m-1].name=f;
      book[m-1].score=1;
    }
    for(int i=0;i<101;i++)
    {
      for(int j=0;j<book[i].score;j++)
      {
        printf("%s%d ",book[i].name,i+1);
      }
    }
    getchar();
    getchar();
    return 0;
}
