$('#likes').click(function(){
    var catid;
    catid = $(this).attr('data-catid');
    $.get('/rango/like_category/', {category_id: catid}, function(response_data){
        $('#like_count').html(response_data);
        $('#likes').hide();
    });
});

$('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/rango/suggest_category', {suggestion: query}, function(response_data){
        $('#cats').html(response_data)
    });

});


$('#addPageModal').find('.addpage').click(function(){
    var title = $("#title-name").val()
    var url = $("#url-text").val()
    var catid = $(this).attr('data-catid')
    $.get('/rango/auto_addpage/', {category_id: catid, title: title, url: url}, function(data){
        if(data != 'error') {
            $('#pages').html(data)
            $('.addpage-close').click()
        }

    });
});
