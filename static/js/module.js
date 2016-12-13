$('#addmoduleform').submit(function (event) {
    event.preventDefault();
    var form = $(this);
    $('#addModule').modal('hide');
    $.ajax({
        type:form.attr('method'),
        url:form.attr('action'),
        data:form.serialize(),
        success:function(data){ alert(data); },
        fail:function(){ alert('增加模块失败');}
    });
});

function delmodule(module){
    $('#myModalModule'+module).modal('hide');
    $.ajax({
        type:'post',
        url:'/api/delmodule',
        data:'module='+module,
        success:function(){ $('#myModalok').modal('show') },
        error:function(){ alert('failed!'); }
    });
}


