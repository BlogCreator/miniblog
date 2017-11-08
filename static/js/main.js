var xmlhttp;
var count;
var json;
var myBody=document.getElementsByClassName("my_body")[0];
var bu='<div class="bodyAll">\
<div class="an_l_title">\
  <h3></h3>\
  <span></span>\
  </div>\
 <div class="an_l_body">\
   <a href="#">\
     <img alt="">\
   </a>\
   <div class="content">\
   </div>\
   <div class="read">阅读全文>>\
   </div>\
</div>\
<div class="an_l_foot">\
  <p>\
    时间:<span></span>\
    作者:<span>cml</span>\
    个人博客:<span></span>\
  </p>\
</div>\
</bodyAll>';
//加载类别
var sContent=document.getElementsByClassName("s_content")[0];
var xml=new XMLHttpRequest();
xml.onreadystatechange=function(){
  if(xml.status==200&&xml.readyState==4){
    var json=JSON.parse(xml.responseText).result;
    for(var i=0;i<json.length;i++)
    {
      if(i%2==0)
      sContent.innerHTML+='<div class="s_content1"></div>';
      else{
        sContent.innerHTML+='<div class="s_content2"></div>';
      }
      var s=sContent.children[i];
      s.innerText=json[i];
    }
  }
}
xml.open("post","/interface/get_cls",true);
xml.send();
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
        //加载文章目录
        var titleIndex1=document.getElementsByClassName("title_index1")[0].getElementsByTagName("li");
        titleIndex1[i].innerHTML=json[i].title;
        //加载标题,图片,描述,日期
        title.innerHTML=json[i].title;
        var img=document.getElementsByClassName("an_l_body")[i].getElementsByTagName("img")[0];
        img.src="/"+json[i].pic;
        var desc=document.getElementsByClassName("content")[i];
        var content=json[i].desc;
        desc.innerHTML=content;
        var foot=document.getElementsByClassName("an_l_foot")[i].getElementsByTagName("span");
        foot[0].innerHTML=json[i].date[0]+"-"+json[i].date[1]+"-"+json[i].date[2];
        foot[2].innerHTML=json[i].cls;
      }
      search(json);

      //点击后获取全部文章
      more.onclick=function(){
        myBody.style.overflow="auto";
        myBody.style.height="100%";
        more.style.display="none";
      }
    }
  }
}
xmlhttp.open("post","/interface/get_recent_article",true);
xmlhttp.send(10);

//搜索框
function search(json){
  var s=Array.prototype.slice.call(sContent.children);
  console.log(json.length);
  s.forEach(function(ele,index){
    console.log(ele);
    ele.onclick=function(){
      var value=ele.innerText;
      for(var i=0;i<json.length;i++){
        if(value!=json[i].cls){
          console.log("!!!");
          myBody.children[i].style.display="none";
        }
      }
      if(myBody.innerHTML==""){
        console.log("err");
        myBody.innerHTML="对不起您搜索的专栏暂不存在";
      }
    }
  });
}
var box=document.getElementsByClassName("box");
//var box_a=box.getElementsByTagName("a");
//自动旋转框
var p=0;
var container=document.getElementById('container');
setInterval(function(){
  p++;
  var s=container.style.transform;
  var d=s.replace(/(\d{1,})/,72*p);
  container.style.transform=d;
},2000);
