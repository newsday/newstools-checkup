
binner = function(a, q) {
    /////////
    // q binner:
    // for a given question,
    // examines a politician's answer,
    // and puts 'em in the right bin.
    /////////
    return(function(obj) {
      return a[obj.qas[q]];
    });
};

$question_box = $('.question-wrapper');
$question = $('.question-title');

bin_trigger_height = undefined;
function get_bin_trigger_height(update) {
  if(_.isUndefined(bin_trigger_height) || !_.isUndefined(update)) {
    bin_trigger_height = $("#header").outerHeight(true) + $('.question-title').outerHeight(true);
    // console.log("  update bin trigger height @" + bin_trigger_height);
    return bin_trigger_height;
  } else {
    // console.log("    fetch bin trigger height @" + bin_trigger_height);
    return bin_trigger_height;
  }
}

update_title = function($title, height) {
  $parent = $title.parent();
  $title.css('width', $parent.width())
            .css('top', height)
            .css('left', $parent.offset().left + parseInt($parent.css("padding-left"), 10));
};

// create waypoints
create_waypoints = function() {
   $question_box.waypoint(function(direction) {
        $this = $(this);
        $title = $this.find(".question-title");
        if(direction == "down") {
          $title.addClass('stuck');
          update_title($title, $("#header").outerHeight(true) || 0);
               // .css("top", )
               // .css("left", $question_box.offset().left + parseInt($question_box.css("padding-left"), 10));
        } else if(direction == "up") {
          $title.removeClass('stuck');
        }
      }, {
        offset: function() { /*console.log("  question-title.offset()");*/ return $("#header").outerHeight(true) || 0; }
      });
   
   /* question titles */
    $(".bin-wrapper").waypoint(function(direction) {
        $title = $(this).find(".title");
        if(direction == "down") {
          // console.log("STICK: .bin-wrapper .title");
          $title.addClass("stuck");
          update_title($title, $("#header").outerHeight(true) + $('.question-title').outerHeight(true));
        }
        else if(direction == "up") {
          // console.log("UNSTICK: .bin-wrapper .title");
          $title.removeClass("stuck");
        }
      }, {
        offset: function() { /*console.log("  #" + $(this).attr('id') + " .title.offset()");*/ return get_bin_trigger_height(); }
      }
    );
};

// Code to run once question resizing is complete. We need this outside of
// the main custom_sizes function to force a smart debounce, since
// $.waypoints('refresh') isn't the cheapest (and isn't something that has to
// run while resizing is ongoing, unlike much of the rest of custom_sizes).

question_resized = _.debounce(function() {
    // console.log(" question resize done");
    // get_bin_trigger_height(true);
    $.waypoints('refresh');
  }, 500);

// Custom-size the page's sticky elements
custom_sizes = function() {
    // console.log("RUN: CUSTOM_SIZES");
    
    $bin_wrapper_titles = $(".bin-wrapper .title");
    
    $clear = $(".question-wrapper,.question-title,.bin-wrapper .title");
    
    // console.log(" starting question resize");
    
    qheight = $question.outerHeight(true);
    $question_box.stop().animate({
      'height': qheight
    }, 200, question_resized);
    $question.css('width', $question_box.width());
    
    if(!window.isMobile.any() && $(window).width() > 768) {
      // question_trigger_height = $("#header").outerHeight(true) || 0;
      
      $.waypoints('enable');
      
      update_title($(".question-title"), $("#header").outerHeight(true) || 0);
      
      _($bin_wrapper_titles).each(function(element, index, list) {
        update_title($(element), get_bin_trigger_height(true));
      });
    } else {
      // mobile browsers and too-small windows
      $.waypoints('disable');
      $clear.css("top", "").css("left", "").css("width", "").removeClass("stuck");
    }
};

function scroll_up() {
    // $("html, body").animate({ scrollTop: $('.question-leadin').offset().top-75}, 150, callback);
    $("html, body").scrollTop($('.question-leadin').offset().top-75);
}

$(document).ready(function() {
    container = "#checkup";
    $container = $(container);
    $content = $(".center-content");
  
    // fetch question-settings
    $.getJSON("overview_feed.json", function(d) {
      
  /*******
   * $.CheckUp()
   *******/
  
    // jquery.CheckUp settings
    var settings = {
      target: container,
      json: document.URL.split('#')[0] + "feed.json",
      bin_template: $("#bin_template").html(),
      box_template: $("#box_template").html(),
      post_update: function() { /*console.log("post_update: CUSTOM_SIZES");*/ custom_sizes(); },
      bin_holder: "#bin-holder",
      viz: []
    };
    
    // create viz for each setting
    _(d.questions).each(function(q, key, list) {
      // ONCE MODELS IN PLACE:
      if(q.visualize) {
        settings.viz.push({
          question: q.question,
          explanation: q.explanation,
          directed_to: q.directed_to,
          bins: q.bins,
          binner: binner(d.bin_map, q.question)
        });
      }
    });
    
  /*******
   * Instance
   *******/
    
    $container.checkup(settings);
    $(".control-prev").hide();
    $content.fadeIn(1000);
   
  /*******
   * Paginate
   *******/
    
    animating = false;
    function switch_viz(pg, animation, callback, text_update) {
      if(_(callback).isUndefined()) { callback = function() {}; }
      if(_(text_update).isUndefined()) { text_update = function() {}; }
      animating = true;
      scroll_up();
      $container.checkup().switch_viz(pg, animation, function() { /*console.log("switch_viz(end): CUSTOM_SIZES");*/ custom_sizes(); callback(); animating = false; }, text_update);
    }
    
    pg = 0; max_pg = settings.viz.length;
    function next() {
      if(animating) return false;
      
      pg += 1;
      if(pg >= max_pg) {
        $(".center-content").animo({ animation: 'fadeOutLeftBig', duration: 0.3, keep: true }, function() {
          window.location = $("#checkup").data('data')['first_assignment'];
        });
      } else {
        animate = { in: in_right, out: out_left };
        switch_viz(pg, animate, function() {}, function() {
          if(pg === 1) {
            // show prev button on second page
            $(".control-prev").fadeIn();
            $(".control-tiny-text").text("QUESTION");
          } else if(pg === max_pg - 1) {
            $(".control-big.control-next .control-label").html("Read their<br>responses");
            $(".control-tiny-text").html("QUESTION &nbsp; &nbsp; | &nbsp; &nbsp; RESPONSES");
          } else {
            $(".control-tiny-text").text("QUESTION");
          }
        });
      }
      return false;
    }
    
    function prev() {
      if(animating) return false;
      
      pg -= 1;
      
      animate = { in: in_left, out: out_right };
      switch_viz(pg, animate, function() {}, function() {
        if(pg < max_pg - 1) {
          $(".control-big.control-next .control-label").html("Next<br>Question");
          $(".control-tiny-text").text("QUESTION");
        }
        if(pg===0) {
          // hide prev button on first page
          $(".control-prev").fadeOut();
          $(".control-tiny-text").text("NEXT QUESTION");
        } else {
          $(".control-tiny-text").text("QUESTION");
        }
      });
      
      return false;
    }
    
    $(".control-prev").click(prev); $(".control-next").click(next);
    
  /*******
   * CustomSize()
   *******/
    
    if(!window.isMobile.any()) {
        $(window).resize(function() {
          // console.log("... resize");
          custom_sizes();
          scroll_up();
        });
    } else {
      // yes, this distinction shouldn't exist. but it does.
      // iOS 6 devices fire resizes basically at random sometimes,
      // and we can't have the page leaping upwards at random.
      // additionally we can't do custom_sizes on orientation change because
      // it triggers before the page content reflows and the sizes change.
      // life is hard sometimes. // ap
      $(window).bind('orientationchange', scroll_up);
      $(window).resize(custom_sizes);
    }
    // $(document).ready(custom_sizes);
    create_waypoints();
    custom_sizes();
    $(window).load(function() { /*console.log("window(load):");*/ custom_sizes(); });
    
  }); // getJSON(overview_feed.json)
}); // $(document).ready
