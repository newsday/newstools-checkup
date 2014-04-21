$(document).ready(function() {
    var $content = $(".center-content");
    
    $center = $(".center-content");
    $center.removeClass("center-content-init");
    $center.animo({ animation: in_right, duration: 0.4 });
    
    animate = {
        backward: { in: in_left, out: out_right },
        forward: { in: in_right, out: out_left }
    };
    reverse = { backward: 'forward', forward: 'backward' };
    
    function make_buttons() {
        var $btn = $(this);
        
        if(!$btn.hasClass("control-next")) { dir = "backward"; } else { dir = "forward"; }
        
        url = $btn.attr("href");
        
        if(_(["Back to theQuestions", "QUESTIONS"]).contains($btn.find(".control-label").text())) {
            $("html, body").animate({ scrollTop: 0}, 150, function() {
                $content.animo({ animation: animate[dir].out, duration: 0.4, keep: true }, function() {
                    window.location.href = url; // + "#last";
                });
            });
        } else {
            History.pushState({ dir:  dir}, null, url);
        }
        return false;
    }
    
    $(".control").click(make_buttons);
    
    
    // after a new page is loaded
    function render_page(responseText, textStatus, XMLHttpRequest) {
        var state = History.getState();
        
        $content = $(".center-content");
        
        // Display $content
        if(state.data.dir) {
            $content.animo({ animation: animate[state.data.dir].in, duration: 0.7, keep: true });
        } else {
            $content.animo({ animation: animate['backward'].in, duration: 0.7, keep: true });
        }
            
        $content.removeClass("center-content-init");
        
        // Re-set button press events
        $(".control").click(make_buttons);
        
        // Re-render Twitter buttons
        $.ajax({ url: 'http://platform.twitter.com/widgets.js', dataType: 'script', cache:true});
        
        // Extract metadata from new page
        $newpg = $(responseText);
        title = $newpg.filter("title").text();
        
        // Update metadata
        $("meta").remove();
        $("head").append($newpg.filter("meta"));
        document.title = title;
        
        $('#header,.alert').localScroll({ 'offset': -48 });
        
        // Site-specific hook
        page_load(url, title);
        
        // this doesn't work, but we need something like it.
        // state.data.dir = reverse[state.data.dir];
        state.data.ct += 1;
    }
    
    // // Bind to StateChange Event
    History.Adapter.bind(window,'statechange',function() {
        var state = History.getState();
        
        $("html, body").animate({ scrollTop: 0}, 150, function() {
            // pull to top of page
            if(state.data.dir) {
                $content.animo({ animation: animate[state.data.dir].out, duration: 0.4, keep: true }, function() {});
            } else {
                $content.animo({ animation: animate['backward'].out, duration: 0.4, keep: true }, function() {});
            }
            
            // load new content
            $("#bodyContent").load(state.url + " #bodyContent > *", render_page);
        });
    });
});