$('#addnodeform').submit(function (event) {
    event.preventDefault();
    var form = $(this);
    $('#myModal').modal('hide');
    $.ajax({
        type:form.attr('method'),
        url:form.attr('action'),
        data:form.serialize(),
        success:function(data){ alert(data); },
        fail:function(){ alert('增加节点失败');}
    });
});

function delnode(hostname){
    var node = hostname
    $('#myModalnode'+node).modal('hide');
    $.ajax({
        type:'post',
        url:'/api/delnode',
        data:'node='+node,
        success:function(){ $('#myModalok').modal('show') },
        error:function(){ alert('failed!'); }
    });
}


