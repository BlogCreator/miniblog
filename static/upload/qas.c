#include <stdio.h>
#include <string.h>
struct queue{
  int a[101];
  int head;
  int tail;
};
struct stack{
  int b[101];
  int top;
};
int main()
{
  struct queue q,q1;
  struct stack s;
  int n,m,book[10];
  for(int i=1;i<10;i++)
  {
    book[i]=0;
  }
  q.head=0,q1.head=0;
  q.tail=0,q1.tail=0;
  s.top=0;
  for(int i=0;i<6;i++)
  {
    scanf("%d",&q.a[q.tail]);
    q.tail++;
  }
  for(int i=0;i<6;i++)
  {
    scanf("%d",&q1.a[q1.tail]);
    q1.tail++;
  }
  int qi,q1i;
  while(q.head<q.tail&&q1.head<q1.tail)
  {
    qi=q.a[q.head];
    if(book[qi]==0)
    {
        s.b[s.top]=qi;
        s.top++;
        q.head++;
        book[qi]=1;
    }
    else{
      q.head++;
      q.a[q.tail]=qi;
      q.tail++;
      while(s.b[s.top-1]!=qi)
      {
        book[s.b[s.top-1]]=0;
        q.a[q.tail]=s.b[s.top-1];
        q.tail++;
        s.top--;
      }
        book[s.b[s.top-1]]=0;
        q.a[q.tail]=s.b[s.top-1];
        q.tail++;
        s.top--;
    }
    if(q.head==q.tail){break;}
    q1i=q1.a[q1.head];
    if(book[q1i]==0)
    {
        s.b[s.top]=q1i;
        s.top++;
        q1.head++;
        book[q1i]=1;
    }
    else{
      q1.head++;
      q1.a[q1.tail]=q1i;
      q1.tail++;
      while(q1i!=s.b[s.top-1])
      {
        book[s.b[s.top-1]]=0;
        q1.a[q1.tail]=s.b[s.top-1];
        q1.tail++;
        s.top--;
      }
      book[s.b[s.top-1]]=0;
      q1.a[q1.tail]=s.b[s.top-1];
      q1.tail++;
      s.top--;
    }
  }
    if(q1.head==q1.tail)
    {
      printf("heng win\n");
      printf("小heng的手牌是:");
      for(int i=q.head;i<q.tail-1;i++)
      {
        printf(" %d",q.a[i]);
      }
      if(s.top>0)
      {
        printf("牌是:");
        for(int i=0;i<s.top;i++)
        {
          printf(" %d",s.b[i]);
        }
      }
      else{
        printf("桌子上没有牌了");
      }
    }
    else
    {
      printf("ha win\n");
      printf("小哈的手牌是:");
      for(int i=q1.head;i<q1.tail-1;i++)
      {
        printf(" %d",q1.a[i]);
      }
      if(s.top>0)
      {
        printf("\n的牌是:");
        for(int i=0;i<s.top;i++)
        {
          printf(" %d",s.b[i]);
        }
      }
      else{
        printf("桌子上没有牌了");
      }
  }
  return 0;

}
