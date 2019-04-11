$(function(){
    $("body").fadeIn(1000);
    $(".container").fadeIn().css({top:100,position:'relative'}).animate({top:0}, 500, function() {});
});