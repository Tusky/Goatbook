$(document).ready(function(){
    $('#profile').click(function(){
        $('.triangle_down, #profile').toggleClass('active');
        $('#profile_options').toggle();
    })
})