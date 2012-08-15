$(document).ready(function(){
    $('#profile').click(function(){
        $('.triangle_down, #profile').toggleClass('active')
        $('#profile_options').toggle()
    })

    $('#search_box').keyup(function(ev){
        if(ev.keyCode != 38 && ev.keyCode != 40 && ev.keyCode != 13 ){
            ev.preventDefault();
            var len=$(this).val().length
            if( len > 0){
                $.ajax({
                    url:        "/json/"+$(this).val(),
                    success:    function(data) {
                        $('#search_results ul li').remove()
                        $.each(data, function(index,value){
                            $('#search_results ul').append('<li><a href="/profile/'+value['username']+'">'+value['fullname']+'</a></li>')
                            if( index == 0 )
                                $('#search_results ul li:first').addClass('current');
                        })
                    }
                } )
                $('#search_results').show()
            }else{
                $('#search_results').hide()
            }
        }
    }).blur(function() {
        $(document).unbind('keydown', disableArrowKeys);
    }).focus(function(){
        $(document).bind('keydown', disableArrowKeys);
    })

    $('#search_box').on('keyup',function(ev){
        ev.preventDefault()
        if( ev.keyCode == 38 && $('li.current').prev().is('li') ){
            ev.preventDefault();
            $('li.current').removeClass('current').prev().addClass('current')
        }else if( ev.keyCode == 40 && $('li.current').next().is('li') ){
            ev.preventDefault();
            $('li.current').removeClass('current').next().addClass('current')
        }else if( ev.keyCode == 13 ){
            window.location = $("li.current a").attr("href");
        }
    })
})

var ar = new Array(13, 38, 40);
var disableArrowKeys = function(e) {
    if ($.inArray(e.keyCode, ar)>=0) {
        e.preventDefault();
    }
}