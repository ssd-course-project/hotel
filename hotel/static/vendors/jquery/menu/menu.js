$(function() {

    $('ul.menu > li').hover(
        function(){
            $(this).find('ul.menu__list').fadeIn(200);

        }, function() {
            $(this).find('ul.menu__list').fadeOut(200);

    });
});
