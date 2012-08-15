$(document).ready(function(){
    $('#profile').click(function(){
        $('.triangle_down, #profile').toggleClass('active')
        $('#profile_options').toggle()
    })

    $('#search_box').keyup(function(){
        var len=$(this).val().length
        if( len > 0){
            $.ajax({
                url:        "/json/"+$(this).val(),
                success:    function(data) {
                    $('#search_results ul li').remove()
                    $.each(data, function(index,value){
                        $('#search_results ul').append('<li><a href="/profile/'+value['username']+'">'+value['fullname']+'</a></li>')
                    })
                }
            } )
            $('#search_results').show()
        }else{
            $('#search_results').hide()
        }
    })

})