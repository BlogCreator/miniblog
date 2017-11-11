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
    作者:<span>cml</span>\
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
//中间主内容动态加载
function getContent(json){
  var count=json.length;
  var titleIndex1=document.getElementsByClassName("title_index1")[0];
  titleIndex1.innerHTML="";
  console.log(count);
  if(count==0){myBody.innerHTML="对不起你搜索的标题不存在"}
  for(var i=0;i<count;i++){
    myBody.innerHTML+=bu;
    var title=document.getElementsByClassName("an_l_title")[i].getElementsByTagName("h3")[0];
    //加载文章目录
    titleIndex1.innerHTML+='<li><a href="#"></a></li>';
    var titleText=titleIndex1.getElementsByTagName("a")[i];
    titleText.innerText=json[i].title;
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
}
//hello对象存储所有方法
function hello(){
  this.getClass();
  this.reveal();
  this.getLoading();
  this.access();
  this.rank();
}
hello.prototype={
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
      clickSearch();
    });
    //点击某类别后显示内容或点击搜索框出现的内容
    function clickSearch(){
      var sea=document.getElementsByClassName("search")[0];
      var btn=sea.getElementsByTagName("button")[0];
      btn.onclick=function(){
        var value=sea.getElementsByTagName("input")[0].value;
        self.searchTitle(value,self.readme);
      }
      for(var i=0;i<sContent.children.length;i++){
        (function(u){
            sContent.children[u].onclick=function(){
            self.search(this.innerText,self.readme);
          }
        })(i);
      }
    }
  },
  //加载后显示
  getLoading:function(){
    var self=this;
    myAjax("post","/interface/get_recent_article","application/x-www-form-urlencoded","limit:5",function(cl){
        var length=cl.result.length;
        var cl=cl.result;
        getContent(cl);
        self.showornot(length);
        self.readme();
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
      var titleIndex=document.getElementsByClassName("title_index")[0].getElementsByTagName("li");
      titleIndex[i].getElementsByTagName("a")[0].innerText=cl[i].title;
      titleIndex[i].getElementsByTagName("i")[0].innerText=cl[i].click;
      }
    })
  },
  //点击阅读
  readme:function(){
    var self=this;
    var r=myBody.getElementsByClassName("read");
    for(var i=0;i<r.length;i++){
      (function(s){
          r[s].onclick=function(){
          //event.stopPropagation();
          var title=document.getElementsByClassName("an_l_title")[s].getElementsByTagName("h3")[0].innerText;
          window.open("../instenct/"+title);
          self.addClick(title);
          myBody.innerHTML="";
          myAjax("post","/interface/get_article","application/x-www-form-urlencoded","title="+title,function(cl){
            var cl=cl.result;
            var length=cl.length;
            myBody.innerHTML='<div class="mymargin">'+cl[0].content+'</div>';
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
        }
      })(i);
    }
    self.showornot(r.length);
    //more.style.display="none";
   //myBody.style.height="auto";
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
      getContent(cl);
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
      getContent(cl);
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
      name="匿名";
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
    //console.log("@@@");
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
      /*不可以跟getReivew函数并列　否则只能在没有评论时评论　有评论时不触发onclick函数
      　应该是异步的问题 ,现在对这部分差点儿理解
      */
      btn.onclick=function(event){
        console.log("!!");
        event.stopPropagation();
        console.log(title);
        var value=document.getElementsByTagName("textarea")[0].value;
        var name=document.getElementsByClassName("review_name")[0].getElementsByTagName("input")[0].value;
        self.myreview(name,title,value);
      }
    });
  }
}
window.onload=function(){
  var me=new hello();
}
