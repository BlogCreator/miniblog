#include <stdio.h>
struct queue{
  int x;
  int s;
};
int main()
{
  int n,m,s,end,a,b,e[50][50],book[50]={0};
  scanf("%d%d%d%d",&n,&m,&s,&end);
  for(int i=0;i<n;i++)
  {
    for(int j=0;j<n;j++)
    {
      if(i==j){e[i][j]=0;}
      else{
        e[i][j]=99999;
      }
    }
  }
  for(int i=0;i<m;i++)
  {
    scanf("%d%d",&a,&b);
    e[a-1][b-1]=1;
    e[b-1][a-1]=1;
  }
  struct queue que[1000];
  int head=0,tail=0,flag=0;
  que[tail].x=s;
  que[tail].s=0;
  book[s]=1;
  tail++;
  while(head<tail)
  {
    int x=que[tail].x;
    for(int i=0;i<n;i++)
    {
      if(e[x][i]==1&&book[i]==0)
      {
        book[i]=1;
        que[tail].s=que[head].s+1;
        tail++;
      }
      if(que[tail-1].x==end)
      {
        flag=1;
        return ;
      }
    }
    if(flag==1){break;}
    head++;
  }
  printf("%d",que[tail-1].s);
}
