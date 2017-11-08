#include <stdio.h>
int main(){
  int book[10]={0},dis[10],n,m,e[10][10],a,b,c,min,o;
  scanf("%d%d",&n,&m);
  for(int i=0;i<n;i++)
  {
    for(int j=0;j<n;j++)
    {
      if(i==j){
        e[i][j]=0;
      }
      else{
        e[i][j]=99999;
      }
    }
  }
  for(int i=0;i<m;i++)
  {
    scanf("%d%d%d",&a,&b,&c);
    e[a-1][b-1]=c;
  }
  book[0]=1;
  for(int i=0;i<n;i++)
  {
    dis[i]=e[0][i];
  }
  for(int i=0;i<n-1;i++)
  {
    min=99999;
    for(int j=0;j<n;j++)
    {
      if(book[j]==0)
      {
        if(min>dis[j])
        {
          min=dis[j];
          o=j;
        }
      }
    }
    book[o]=1;
    for(int v=0;v<n;v++)
    {
      if(e[o][v]!=99999)
      {
        if(dis[o]+e[o][v]<dis[v])
        {
          dis[v]=dis[o]+e[o][v];
        }
      }
    }
  }
  for(int i=0;i<n;i++)
  {
    printf("%d ",dis[i]);
  }

}
