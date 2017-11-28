class ajax{
    constructor(){}
    send(kargs){
        var _default = {method:'get'}
        var xhr = new XMLHttpRequest();

        if(kargs.method)
            xhr.open(kargs.method,kargs.url);
        else xhr.open(_default.method,'/');

        for(var k in kargs.head){
            xhr.setRequestHeader(k, head.k);
        }

        if(kargs.body)
            xhr.send(body);
        else xhr.send('');

        var callback = kargs.callback;
        xhr.onreadystatechange = function(){
            if(xhr.readyState === XMLHttpRequest.DONE&&xhr.status === 200){
                callback(xhr.responseText);
            }
        }

    }
}
var getInfo_global = new Object();
var myajax=new ajax();
myajax.send({
    url:'/interface/info',
    method:'post',
    callback:function(response){
        r = JSON.parse(response);
        getInfo_global.__proto__.callback(r);
    }
})
