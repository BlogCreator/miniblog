var myBody=document.getElementsByClassName("my_body")[0];
var sContent=document.getElementsByClassName("s_content")[0];
var more=document.getElementsByClassName("more")[0];
//文章主题内容
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
   <div class="read"><a href="">阅读全文>></a>\
   </div>\
</div>\
<div class="an_l_foot">\
  <p>\
    时间:<span></span>\
    作者:<span></span>\
    个人博客:<span></span>\
  </p>\
</div>\
</bodyAll>';
//ajax请求获取json数据
function myAjax(method,path,head,content,callback){
  var xml=new XMLHttpRequest();
  xml.onreadystatechange=function(){
      if(xml.status==200&&xml.readyState==4){
      var json=JSON.parse(xml.responseText);
      if(typeof callback==="function"){
        callback(json);
      }
    }
  }
  xml.open(method,path,true);
  if(head!=""){
    xml.setRequestHeader("Content-Type",head);
  }
  xml.send(content);
}
//hello对象存储所有方法
function hello(){}
hello.prototype={
  //加载评论(在评论区使用)
  getAllReview:function(){
    var self=this;
    var arr=window.location.href.split("/");
    var title=arr[arr.length-1];
    myAjax("post","/interface/get_article","application/x-www-form-urlencoded","title="+title,function(cl){
      var cl=cl.result;
      var length=cl.length;
      //异步添加评论区
      myBody.innerHTML+='<div class="reivew">\
        <textarea class="review_content" placeholder="留下你的评论吧。。。"></textarea>\
        <div class="review_name">你的名字:<input type="text" required/></div>\
        <div class="re_btn"></div>\
      </div>\
      <div class="loadReview">\
        <div class="review_title"><span>评论</span>\
          <div class="review_number"><i></i>条评论</div>\
        </div>\
      </div>\
      <div class="allReview"></div>'
      self.getReview(title);
    });
    more.style.display="none";
    myBody.style.height="auto";
  },
  //加载文章目录
  getIndex:function(json){
    var titleIndex1=document.getElementsByClassName("title_index1")[0];
    for(var i=0;i<json.length;i++){
      var title=json[i].title;
      titleIndex1.innerHTML+="<li><a class=\"indexName\"></a></li>";
      titleIndex1.getElementsByTagName("a")[i].href="/interface/article/"+title;
      var indexName=document.getElementsByClassName("indexName")[i];
      indexName.innerText=title;
    }
  },
  //中间主内容动态加载
  getContent:function(json){
    var count=json.length;
    if(count==0){myBody.innerHTML="对不起你搜索的标题不存在"}
    for(var i=0;i<count;i++){
      myBody.innerHTML+=bu;
      //加载标题,图片,描述,日期
      var htitle=document.getElementsByClassName("an_l_title")[i].getElementsByTagName("h3")[0];
      htitle.innerText=json[i].title;
      var img=document.getElementsByClassName("an_l_body")[i].getElementsByTagName("img")[0];
      img.src="/"+json[i].pic;
      var desc=document.getElementsByClassName("content")[i];
      var content=json[i].desc;
      desc.innerHTML=content;
      var foot=document.getElementsByClassName("an_l_foot")[i].getElementsByTagName("span");
      foot[0].innerHTML=json[i].date[0]+"-"+json[i].date[1]+"-"+json[i].date[2];
      foot[1].innerHTML=json[i].author;
      foot[2].innerHTML=json[i].cls;
    }
  },
  clickSearch:function(){
    var self=this;
    var sea=document.getElementsByClassName("search")[0];
    var btn=sea.getElementsByTagName("button")[0];
    btn.onclick=function(){
      var value=sea.getElementsByTagName("input")[0].value;
      self.searchTitle(value,p);
    }
    //console.log(sContent.children.length);
    //加载后才有监听函数 且需要一直监听,故需要callback
    for(var i=0;i<sContent.children.length;i++){
      (function(u){
          sContent.children[u].onclick=function(){
          //当点击后r的长度改变,监听事件需要重新刷新,回调函数做参数则不会刷新
          self.search(this.innerText,p);
        }
      })(i);
    }
    //监听read的事件封装成函数,方便回调
    function p(){
      var r=myBody.getElementsByClassName("read");
      for(var i=0;i<r.length;i++){
        (function(s){
            r[s].onclick=function(){
            var title=document.getElementsByClassName("an_l_title")[s].getElementsByTagName("h3")[0].innerText;
            //需要先增加点击量再跳转
            self.addClick(title);
            window.open("/interface/article/"+title);
          }
        })(i);
      }
    }
    p();
    self.showornot(r.length);
  },
  //加载类别   在加载完类别后才有点击类别事件
  getClass:function(){
    var self=this;
    myAjax("post","/interface/get_cls","","",function(cl){
      var length=cl.result.length;
      var cl=cl.result;
      for(var i=0;i<length;i++)
      {
        if(i%2==0)
        sContent.innerHTML+='<div class="s_content1"></div>';
        else{
          sContent.innerHTML+='<div class="s_content2"></div>';
        }
        var s=sContent.children[i];
        s.innerText=cl[i];
      }
    });
  },
  //自动旋转框
  reveal:function(){
    var box=document.getElementsByClassName("box");
    var p=0;
    var container=document.getElementById('container');
    setInterval(function(){
      p=p+3;
      var s=container.style.transform;
      var d=s.replace(/(\d{1,})/,p);
      container.style.transform=d;
    },100);
  },
  //加载后显示
  getLoading:function(){
    var self=this;
    myAjax("post","/interface/get_recent_article","application/x-www-form-urlencoded","limit:5",function(cl){
        var length=cl.result.length;
        var cl=cl.result;
        self.getContent(cl);
        self.getIndex(cl);
        self.showornot(length);
    });
  },
  //获取访问量
  access:function(){
    myAjax("post","/interface/get_access","","",function(cl){
      var cl=cl.result;
      var vis=document.getElementsByClassName("vis")[0];
      vis.innerText="  "+cl;
    });
    var myDate=new Date();
    var year=myDate.getFullYear();
    var month=myDate.getMonth()+1;
    var day=myDate.getDate();
    var allDate=year+"-"+month+"-"+day;
    console.log(allDate);
    myAjax("post","/interface/get_access","application/x-www-form-urlencoded","start="+allDate+"&end=",function(cl){
      var cl=cl.result;
      var vis=document.getElementsByClassName("vis")[1];
      vis.innerText="  "+cl;
    });
  },
  //点击排行
  rank:function(){
    myAjax("post","/interface/get_click_article","application/x-www-form-urlencoded","limit:5",function(cl){
      var length=cl.result.length;
      var cl=cl.result;
      for(var i=0;i<length;i++){
      document.getElementsByClassName("title_index")[0].innerHTML+='<li><a href="#">1</a><span>点击量:<i style="color:red"></i></span></li>'
      var titleIndex=document.getElementsByClassName("title_index")[0].getElementsByTagName("li");
      titleIndex[i].getElementsByTagName("a")[0].innerText=cl[i].blog_title;
      titleIndex[i].getElementsByTagName("a")[0].href="/interface/article/"+cl[i].blog_title;
      titleIndex[i].getElementsByTagName("i")[0].innerText=cl[i].number;
      }
    })
  },
  //增加点击量
  addClick:function(title){
    var self=this;
    myAjax("post","/interface/click","application/x-www-form-urlencoded","title="+title,function(cl){
      if(cl.success=="true"){
        self.rank();
      }
    })
  },
  //html加载完成后动态添加搜索框,点击阅读全文

  //点击搜索框后显示内容
  searchTitle:function(text,callback){
    var self=this;
    myAjax("post","/interface/get_article","application/x-www-form-urlencoded","title="+text,function(cl){
      var length=cl.result.length;
      var cl=cl.result;
      myBody.innerHTML="";
      self.getContent(cl);
      self.showornot(length);
      if(typeof callback==="function"){callback()}
    });
  },
  search:function(text,callback){
    var self=this;
    myAjax("post","/interface/get_article","application/x-www-form-urlencoded","cls="+text,function(cl){
      var length=cl.result.length;
      var cl=cl.result;
      myBody.innerHTML="";
      self.getContent(cl);
      self.showornot(length);
      if(typeof callback==="function"){callback()}
    });
  },
  showornot:function(length){
    if(length>3){
      more.style.display="inline";
    }
    else{
      more.style.display="none";
    }
    //点击后获取全部文章
    more.onclick=function(){
      myBody.style.overflow="auto";
      myBody.style.height="100%";
      more.style.display="none";
    }
  },
  //点击评论
  myreview:function(name,title,value){
    if(name==""){
      alert("请留下您的姓名");
      return false;
    }
    var self=this;
    myAjax("post","/interface/comment","application/x-www-form-urlencoded","name="+name+"&title="+title+"&content="+value,function(cl){
        var success=cl.success;
        if(success=='true'){
          alert("评论成功");
          self.getReview(title);
        }
        else {
          alert('评论失败');
        }
    })
  },
  getReview:function(title){
    var self=this;
    myAjax("post","/interface/get_comment","application/x-www-form-urlencoded","title="+title,function(cl){
      console.log(cl);
      var allReview=document.getElementsByClassName("allReview")[0];
      allReview.innerHTML="";
      var result=cl.result;
      var reviewNumber=document.getElementsByClassName("review_number")[0].getElementsByTagName("i")[0];
      console.log(reviewNumber.innerText);
      reviewNumber.innerText=result.length;
      console.log(result.length);
      for(var i=0;i<result.length;i++){
        allReview.innerHTML+='<div class="showReview">\
          <span class="reviewName"></span>\
          <span class="reviewTime"></span>\
          <br>\
          <br>\
          <span class="showContent"></span>\
        </div>'
        var name=result[i].name;
        var content=result[i].content;
        var date=result[i].date[0]+"-"+result[i].date[1]+"-"+result[i].date[2];
        var na=document.getElementsByClassName("reviewName")[i];
        var ti=document.getElementsByClassName("reviewTime")[i];
        var showContent=document.getElementsByClassName("showContent")[i];
        na.innerText=name;
        ti.innerText=date;
        showContent.innerText=content;
      }
      var btn=document.getElementsByClassName("re_btn")[0];
      /*不可以跟getReivew函数并列　否则只能在没有评论时评论　有评论时不触发onclick函数*/
      btn.onclick=function(event){
        console.log("!!");
        event.stopPropagation();
        console.log(title);
        var value=document.getElementsByTagName("textarea")[0].value;
        var name=document.getElementsByClassName("review_name")[0].getElementsByTagName("input")[0].value;
        console.log(name);
        self.myreview(name,title,value);
      }
    });
  },
  setName:function(){
    var fo=document.getElementsByClassName("an_l_foot");
    console.log(fo.length);
    console.log(foot[foot.length-1].getElementsByTagName("span")[1]);
    var la=foot[foot.length-1].getElementsByTagName("span")[1]="孙亚坤";
  }
}
