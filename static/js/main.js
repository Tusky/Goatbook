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
                            $('#search_results ul').append('<li class="searchy"><a href="/profile/'+value['username']+'"><img src="'+value['imageurl']+'">'+value['fullname']+'</a></li>')
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
        $(document).unbind('keydown', disableArrowKeys)
        $('#search_results').hide()
    }).focus(function(){
        $(document).bind('keydown', disableArrowKeys)
        $('#search_results').show()
    })

    $('#search_box').on('keyup',function(ev){
        //TODO: when not selected anything, and pressing buttons, nothing happens, should select either first or last depending on the button pressed
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
    $("#search_results li").live('mouseover',function(){
        $(this).addClass('current');
    }).live('mouseleave',function(){
        $(this).removeClass('current')
    })
})

var ar = new Array(13, 38, 40);
var disableArrowKeys = function(e) {
    if ($.inArray(e.keyCode, ar)>=0) {
        e.preventDefault();
    }
}