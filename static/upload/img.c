#include <stdio.h>
int n,m,e[50][50],book[50]={0},sum=0;
void dfs(int node)
{
  int s=node;
  printf("%d",node+1);
    sum++;
    if(sum==n)
    {
      return ;
    }
  for(int i=0;i<m;i++)
  {
    if(e[s][i]==1&&book[i]==0)
    {
      book[i]=1;
      dfs(i);
    }
  }
}
int main()
{
  scanf("%d%d",&n,&m);
  int a,b;
  for(int i=0;i<n;i++)
  {
    for(int j=0;j<n;j++)
    {
      if(i==j)
      {
        e[i][j]=0;
      }
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
  book[0]=1;
  dfs(0);
}
