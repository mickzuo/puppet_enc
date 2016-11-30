$('#addnodeform').submit(function (event) {
    event.preventDefault();
    var form = $(this);

    $.ajax({
        type:form.attr('method'),
        url:form.attr('action'),
        data:form.serialize(),
        success:function(data){ alert(data); },
        fail:function(){ alert('增加节点失败');}
    });
});
