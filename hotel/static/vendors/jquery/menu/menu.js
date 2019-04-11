$(function() {

    $('ul.menu > li').hover(
        function(){
            $(this).find('ul.menu__list').show(200);

        }, function() {
            $(this).find('ul.menu__list').hide(200);

    });
});
