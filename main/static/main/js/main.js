$(document).ready(function($) {
    "use strict";
    
    $('#container').pinto({
        itemWidth:230,
        gapX:10,
        gapY:10,
        onItemLayout: function($item, column, position) {
        }
    });
    
    $("#pintoInit").click(function(){
        $('#container').pinto();
    });
    
    $("#pintoDestroy").click(function(){
        $('#container').pinto("destroy");
    });
    
    $("#categories-dropdown").click(function(){
        if ($(".categories-hidden").css("display") == 'none'){
            $(".categories-hidden").slideDown();
        } else {
            $(".categories-hidden").slideUp();
        }
    })

});