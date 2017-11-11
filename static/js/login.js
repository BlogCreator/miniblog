//获取发布内容
var btn=document.getElementsByClassName("btn")[0];
btn.onclick=function(){
  var xml=new XMLHttpRequest();
  xml.onreadystatechange=function(){
    var json=JSON.parse(xml.responseText);
    console.log(json.success);
    if(json.success=="true"){
      var login=document.getElementsByClassName("login")[0];
      login.style.marginTop="-160px";
      var sub=document.getElementsByClassName("sub")[0];
      sub.innerHTML='\
        <form action="/interface/publish_article" method="post" enctype="multipart/form-data">\
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
            <input type="text" name="cls">\
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
            <input type="submit" id="submit" class="btn" value="发布">\
          </div>\
        </form>'
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
