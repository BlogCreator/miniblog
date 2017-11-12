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
var myNav=document.getElementsByClassName("my_nav")[0];
var tilt=document.getElementById("tilt");
myNav.onclick=function(){
  tilt.style.display="block";
}
var closeme=document.getElementsByClassName("closeme")[0];
closeme.onclick=function(){
  console.log("!!");
  tilt.style.display="none";
}
