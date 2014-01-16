(function ($) {
    
    animate = {
        'in': 'show',
        'out': 'show'
    };
    
    mapping = {
        'fadeIn': animate['in'],
        'fadeInDown': animate['in'],
        'bounceInRight': animate['in'],
        'bounceInLeft': animate['in'],
        'fadeOut': animate['out'],
        'fadeOutUp': animate['out'],
        'fadeOutRightBig': animate['out'],
        'fadeOutLeftBig': animate['out']
    };
    
    $.fn.animo = function( options, callback ) {
        return this.each(function() {
            if(options === "cleanse") { return false; }
            return $(this)[mapping[options.animation]](1000*options.duration, callback);
        });
    };
    
    $(".center-content").fadeIn(1000);
    
}( jQuery ));