$(document).ready(function() {
    // var $prev_ctl, $next_ctl, $body;
    
    // $prev_ctl = $('#control-prev');
    // $next_ctl = $('#control-next');
    
    // PUT ALL THE STUFF THAT SHOULDN'T LOAD IN IE9 IN HERE
    
    $centerContent = $(".center-content");
    $centerContent.removeClass("center-content-init");
    $centerContent.animo({ animation: in_right, duration: 0.4 });
    
    // if(isMobile.any()) {
    //     $("#bodyContent").swipe({
    //         swipeLeft: function(event, direction, distance, duration, fingerCount) {
    //             $next_ctl.addClass("active");
    //             $next_ctl.click();
    //         },
    //         swipeRight: function(event, direction, distance, duration, fingerCount) {
    //             $prev_ctl.addClass("active");
    //             $prev_ctl.click();
    //         }
    //     });
    // }
});