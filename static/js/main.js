var xmlhttp;
var bu='<div class="an_l_body">\
   <a href="#">\
     <img width="200" height="100" alt="">\
   </a>\
   <div class="content">\
   </div>\
</div>\
<div class="an_l_foot">\
  <p>\
    时间:<span></span>\
    作者:<span>cml</span>\
    <span></span>\
  </p>\
</div>';
//正常加载出的３个文章
if(window.XMLHttpRequest)
{
  xmlhttp=new XMLHttpRequest();
}
xmlhttp.onreadystatechange=function(){
  if(xmlhttp.status==200){
    if(xmlhttp.readyState==4){
      var json=JSON.parse(xmlhttp.responseText).result;
      console.log(json);
      var myBody=document.getElementsByClassName("my_body")[0];
      for(var i=0;i<1;i++){
        myBody.innerHTML+=bu;
        var img=document.getElementsByClassName("an_l_body")[0].getElementsByTagName("img")[0];
        img.src=json[i].file;
        var desc=document.getElementsByClassName("content")[i];
        var content=json[i].desc;
        desc.innerHTML=content;
        var foot=document.getElementsByClassName("an_l_foot")[i].getElementsByTagName("span");
        foot[0].innerHTML=json[i].date.substring(0,10);
        foot[2].innerHTML=json[i].cls;
      }
    }
  }
}
xmlhttp.open("post","/interface/get_recent_article",true);
xmlhttp.send(10);
//点击加载更多后加载其余文章
var more=document.getElementsByClassName("more")[0].getElementsByTagName("a")[0];
more.onclick=function(){
  for(var i=3;i<json.length;i++)
  {
    myBody.innerHTML+=bu;
  }
}
/*
搜索框
var sContent=document.getElementsByClassName("s_content")[0].children;
var s=Array.prototype.slice.call(sContent,0);
s.forEach(function(ele,index){
  ele.onclick=function(){
    for()
  }
});
*/
