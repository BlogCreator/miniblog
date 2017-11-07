var headLink=document.getElementsByClassName("head_link");
for(var i=0;i<headLink.length;i++)
{
  (function(s){
    headLink[s].onclick=function()
    {
      var topCurrent=document.getElementsByClassName("top_current")[0];
      topCurrent.classList.remove("top_current");
      this.classList.add("top_current");
    }
  })(i);
}
用原生js写过的几个小游戏，存储在我的github中
写过自己的个人博客，前端页面用html，css，原生js写的，服务器用nodejs搭建的，包含一些个人的学习生活经历
