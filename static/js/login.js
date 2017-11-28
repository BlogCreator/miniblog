//获取发布内容
var btn=document.getElementsByClassName("btn")[0];
var btn1=document.getElementsByClassName("setBtn")[0]
var sub=document.getElementsByClassName("sub")[0];
var subRight=document.getElementsByClassName("sub_right")[0];
btn.onclick=function(){
  var xml=new XMLHttpRequest();
  xml.onreadystatechange=function(){
    if(xml.status==200&&xml.readyState==4){
      var json=JSON.parse(xml.responseText);
      if(json.success=="true"){
        var login=document.getElementsByClassName("login")[0];
        login.style.marginTop="-150px";
        sub.innerHTML='\
          <form class="myForm" action="/interface/publish_article" method="post" enctype="multipart/form-data">\
            <div>\
              <label>标题</label>\
              <input type="text" name="title">\
            </div>\
            <div>\
              <label></label>\
              <textarea type="textarea" name="desc" placeholder="写下你的描述"></textarea>\
            </div>\
            <div>\
              <label>类别</label>\
              <input class="myCls" type="text" name="cls">\
            </div>\
            <div>\
              <label>文件</label>\
              <input type="file" style="width:243px" name="file">\
            </div>\
            <div>\
              <label>图片</label>\
              <input type="file" style="width:243px" name="pic">\
            </div>\
            <div>\
              <label></label>\
              <input type="button" id="sub" class="btn" value="发布">\
            </div>\
            <div>\
              <label></label>\
              <input type="button" id="mysub" class="mybtn" value="完善我的个人信息">\
            </div>\
          </form>'
          var mybtn=document.getElementsByClassName("mybtn")[0];
          mybtn.onclick=function(event){
            event.stopPropagation();
            sub.style.marginLeft="-150px";
            sub.style.width="600px";
            subRight.style.display="block";
          }
          btn1.onclick=setInfo;
          var subb=document.getElementById("sub");
          subb.onclick=function(){
            var va=document.getElementsByClassName("myCls")[0].value;
            checkCls(va);
          }
        }
    else{
      var error=document.getElementsByClassName("error")[0];
      error.style.display="block";
    }
  }
  }
  xml.open("post","/interface/login",true);
  var username=document.getElementsByClassName("username")[0].value;
  var password=document.getElementsByClassName("passWord")[0].value;
  xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  xml.send("username="+username+"&password="+password);
}
//更新个人信息
function setInfo(){
  var arr=[];
  var d=subRight.getElementsByTagName("div");
  for(var i=0;i<d.length-1;i++){
    arr[i]=d[i].children[1].value;
  }
  var str="name="+arr[0]+"&email="+arr[1]+"&motto="+arr[2]+"&birthday="+arr[3]+"&school="+arr[4];
  var myajax=new XMLHttpRequest();
  myajax.onreadystatechange=function(){
    if(myajax.status==200&&myajax.readyState==4){
      var json=JSON.parse(myajax.responseText);
      console.log()
      if(json.success=="true"){
        alert("保存成功");
      }
      else{
        alert("保存失败");
      }
    }
  }
  myajax.open("post","/interface/set_info",true);
  myajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  myajax.send(str);
}
//检测类别
function checkCls(value){
   var flag=false;
   var myForm=document.getElementsByClassName("myForm")[0];
   var xmlh=new XMLHttpRequest();
   xmlh.onreadystatechange=function(){
     if(xmlh.readyState==4&&xmlh.status==200){
       var cl=JSON.parse(xmlh.responseText).result;
       console.log(value);
       for(var i=0;i<cl.length;i++){
         if(cl[i]==value){
           flag=true;
         }
       }
       if(flag==false){
         addCls(value);
       }
       else{
         myForm.submit();
       }
     }
   }
   xmlh.open("post","/interface/get_cls");
   xmlh.send();
}
//添加类别
function addCls(value){
    var myForm=document.getElementsByClassName("myForm")[0];
    var xmlh=new XMLHttpRequest();
    xmlh.onreadystatechange=function(){
      myForm.submit();
    }
    xmlh.open("post","/interface/create_cls");
    xmlh.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xmlh.send("cls="+value);
}
