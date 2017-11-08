var xmlhttp;
var count;
var json;
var myBody=document.getElementsByClassName("my_body")[0];
var bu='<div class="an_l_title">\
  <h3></h3>\
  <span></span>\
  </div>\
 <div class="an_l_body">\
   <a href="#">\
     <img alt="">\
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
      var more=document.getElementsByClassName("more")[0];
      json=JSON.parse(xmlhttp.responseText).result;
      count=json.length;
      if(count>3){
        more.style.display="inline";
      }
      //console.log(json);
      for(var i=0;i<count;i++){
        myBody.innerHTML+=bu;
        var title=document.getElementsByClassName("an_l_title")[i].getElementsByTagName("h3")[0];
        title.innerHTML=json[i].title;
        var img=document.getElementsByClassName("an_l_body")[0].getElementsByTagName("img")[0];
        img.src=json[i].file;
        var desc=document.getElementsByClassName("content")[i];
        var content=json[i].desc;
        desc.innerHTML=content;
        var foot=document.getElementsByClassName("an_l_foot")[i].getElementsByTagName("span");
        foot[0].innerHTML=json[i].date.substring(0,10);
        foot[2].innerHTML=json[i].cls;
      }
      more.onclick=function(){
        myBody.style.overflow="";
      }
    }
  }
}
xmlhttp.open("post","/interface/get_recent_article",true);
xmlhttp.send(10);
//点击加载更多后加载其余文章
/*
var more=document.getElementsByClassName("more")[0].getElementsByTagName("a")[0];
more.onclick=function(){
  for(var i=3;i<count;i++)
  {
    myBody.innerHTML+=bu;
  }
}
*/
//加载搜索类别
var sContent=document.getElementsByClassName("s_content")[0];
var xml=new XMLHttpRequest();
xml.onreadystatechange=function(){
  if(xml.status==200&&xml.readyState==4){
    var json=JSON.parse(xml.responseText).result;
    for(var i=0;i<count;i++)
    {
      if(i%2==0)
      sContent.innerHTML+='<div class="s_content1"></div>';
      else{
        sContent.innerHTML+='<div class="s_content2"></div>';
      }
      var s=sContent.children[i];
      s.innerText=json[i];
    }
    search();
  }
}
xml.open("post","/interface/get_cls",true);
xml.send();
//搜索框
function search(){
  var flag=false;
  var s=Array.prototype.slice.call(sContent.children);
  console.log(s);
  s.forEach(function(ele,index){
    console.log(ele);
    ele.onclick=function(){
      console.log("success");
      myBody.innerHTML="";
      for(var i=0;i<count;i++){
        if(ele.innerText==json[i].cls){
          flag=true;
          myBody.innerHTML+=bu;
        }
      }
      if(flag==false){
        console.log("err");
        myBody.innerHTML="对不起您搜索的专栏暂不存在";
      }
    }
  });
}
var box=document.getElementsByClassName("box");
//var box_a=box.getElementsByTagName("a");
var p=0;
var container=document.getElementById('container');
container.onclick=function(){
  p++;
  var s=container.style.transform;
  var d=s.replace(/(\d{1,})/,72*p);
  container.style.transform=d;
}
