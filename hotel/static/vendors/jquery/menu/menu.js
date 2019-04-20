$(function() {

    $('ul.menu > li').hover(
        function(){
            $(this).find('ul.menu__list').fadeIn(200).css({'position': 'absolute', 'z-index':'1000'});

        }, function() {
            $(this).find('ul.menu__list').fadeOut(200);

    });
});
