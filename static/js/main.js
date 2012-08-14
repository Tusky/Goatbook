$(document).ready(function(){
    $('#profile').click(function(){
        $('.triangle_down, #profile').toggleClass('active')
        $('#profile_options').toggle()
    })

    $('#search_box').keyup(function(){
        var len=$(this).val().length
        if( len > 0){
            $('#search_results').show()
        }else{
            $('#search_results').hide()
        }
    })
})