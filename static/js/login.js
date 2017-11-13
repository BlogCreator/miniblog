//获取发布内容
var btn=document.getElementsByClassName("btn")[0];
btn.onclick=function(){
  var xml=new XMLHttpRequest();
  xml.onreadystatechange=function(){
    var json=JSON.parse(xml.responseText);
    console.log(json.success);
    if(json.success=="true"){
      var login=document.getElementsByClassName("login")[0];
      login.style.marginTop="-150px";
      var sub=document.getElementsByClassName("sub")[0];
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
        </form>'
        var sub=document.getElementById("sub");
        sub.onclick=function(){
          var va=document.getElementsByClassName("myCls")[0].value;
          checkCls(va);
        }
    }
    else{
      var error=document.getElementsByClassName("error")[0];
      error.style.display="block";
    }
  }
  xml.open("post","/interface/login",true);
  var username=document.getElementsByClassName("username")[0].value;
  var password=document.getElementsByClassName("passWord")[0].value;
  xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
  xml.send("username="+username+"&password="+password);
}
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
