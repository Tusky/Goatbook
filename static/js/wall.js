$().ready(function(){
    $('.opinion .dislike span').each(function(){
        if($(this).text().trim().length == 0){
            $(this).parents('.dislike').hide()
        }
    })
    $('.opinion .like span').each(function(){
        if($(this).text().trim().length == 0){
            $(this).parents('.like').hide()
        }
    })

    $('.options .like span').click(function(){
        var clicked_on = $(this)
        var url = $(this).parents().siblings('.date').children('a').attr('href') + "/like"
        $.ajax({
            url: url,
            success: function(data) {
                switch(data['response']){
                    case "removed":
                        clicked_on.text("Like");
                        doStuff(clicked_on, data['liked_by'], data['hated_by'])
                        break;
                    case "liked":
                        clicked_on.text("Liked");
                        clicked_on.parents('.options').children('.dislike').children('span').text('Dislike')
                        doStuff(clicked_on, data['liked_by'], data['hated_by'])
                        break;
                    default:
                        console.log("error")
                }
            }
        })
    })

    $('.options .dislike span').click(function(){
        var clicked_on = $(this)
        var url = $(this).parents().siblings('.date').children('a').attr('href') + "/dislike"
        var text = clicked_on.parents('.post').find('.opinion .dislike span').text();
        $.ajax({
            url: url,
            success: function(data) {
                switch(data['response']){
                    case "removed":
                        clicked_on.text("Dislike");
                        doStuff(clicked_on, data['liked_by'], data['hated_by'])
                        break;
                    case "disliked":
                        clicked_on.text("Disliked");
                        clicked_on.parents('.options').children('.like').children('span').text('Like')
                        doStuff(clicked_on, data['liked_by'], data['hated_by'])
                        break;
                    default:
                        console.log("error")
                }
            }
        })
    })
})

function doStuff(clicked_on, liked_by, hated_by){
    var likes = liked_by.split(","),
        hates = hated_by.split(","),
        hate_new_text = "",
        like_new_text = "",
        like_counter  = 0,
        hate_counter  = 0,
        like_abbr     = "",
        hate_abbr     = "";
    $.each(likes, function(i){
        if( i < 3 ){
            if(i + 1 == likes.length || i + 1 == 3)
                like_new_text += likes[i];
            else
                like_new_text += likes[i]+", ";
        }else{
            like_counter++;
            if(i + 1 == likes.length)
                like_abbr += likes[i];
            else
                like_abbr += likes[i]+", ";
        }
    })
    $.each(hates, function(i){
        if( i < 3 ){
            if(i + 1 == hates.length || i + 1 == 3)
                hate_new_text += hates[i];
            else
                hate_new_text += hates[i]+", ";
        }else{
            hate_counter++;
            if(i + 1 == hate.length)
                hate_abbr += hates[i];
            else
                hate_abbr += hates[i]+", ";
        }
    })
    if( like_abbr.length != 0 ){
        like_new_text = like_new_text + ' and <abbr title="'+ like_abbr + '">' + like_counter + ' more</abbr>'
    }
    if( hate_abbr.length != 0 ){
        hate_new_text = hate_new_text + ' and <abbr title="'+ hate_abbr + '">' + hate_counter + ' more</abbr>'
    }

    clicked_on.parents('.post').find('.opinion .like span').text(like_new_text)
    clicked_on.parents('.post').find('.opinion .dislike span').text(hate_new_text)

    if(liked_by.length == 0){
        clicked_on.parents('.post').find('.opinion .like').hide();
    }else{
        clicked_on.parents('.post').find('.opinion .like').show();
    }
    if(hated_by.length == 0){
        clicked_on.parents('.post').find('.opinion .dislike').hide();
    }else{
        clicked_on.parents('.post').find('.opinion .dislike').show();
    }
}