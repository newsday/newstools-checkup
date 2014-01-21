(function ($) {
 
    $.fn.checkup = function( options ) {
        var $this, $data, loop;
        
        $this = $(this); $data = $this.data();
        if($data.hasOwnProperty('fns')) { return $data.fns; }
        
        /////////////
        // Helpers //
        /////////////
        
        function get_viz() {
            return $data.viz[$data["active-viz"]];
        }
        
        function get_data(v) {
            return $data[v];
        }
        
        function empty_list_obj(keys) {
            obj = {};
            _(keys).each(function(key) {
                obj[key] = [];
            });
            return obj;
        }
        
        ////////////
        // Render //
        ////////////
        
        function render() {
            data = $data.data;
            
            viz = get_viz();
                        
            function update_bin(value, key, list) {
                bin_val = viz.binner(value);
                
                value.bin = viz.bins[bin_val];
                value.bin_key = bin_val;
            }
            
            _(data.assignments).each(update_bin);
            
            bin_data = _(data.assignments).groupBy('bin_key');
            
            if(_.isUndefined($data.bin_data)) {
                inserts = bin_data;
                removes = empty_list_obj($data.bin_keys);
                $data.bin_data = bin_data;
            } else {
                inserts = empty_list_obj($data.bin_keys);
                removes = empty_list_obj($data.bin_keys);
                
                _($data.bin_keys).each(function(key) {
                    new_data = bin_data[key];
                    current_data = $data.bin_data[key];
                    inserts[key] = _(new_data).difference(current_data);
                    removes[key] = _(current_data).difference(new_data);
                });
            }
                        
            _($data.bin_keys).each(function(key) {
                // for each bin...
                $bin = $("#" + key + "-bin");
                $bin.isotope('reloadItems').isotope();
                
                // start the animation with remove
                if(key in removes && removes[key].length) {
                    removable = _(removes[key]).pluck('key');
                    $("#" + key + "-bin").isotope('remove', $("#" + removable.join(",#")), function() {
                        $("#" + key + "-bin").isotope('reloadItems').isotope();
                    });
                }
            });
            
            _($data.bin_keys).each(function(key) {
                $bin = $("#" + key + "-bin");
                $bin.isotope('reloadItems').isotope();
                
                // then do inserts
                insertable = _(inserts[key]).pluck('box_html');
                if(insertable.length) {
                    $bin.isotope('insert', $(insertable.join('')), function() {
                        $bin.isotope('reloadItems').isotope();
                    });
                } else {
                    $bin.isotope('reloadItems').isotope();
                }
            });
            
            _($data.bin_keys).each(function(key) {
                vizbin = viz.bins[key];
                
                // do any final position updates
                $("#" + key + "-bin").isotope('reloadItems').isotope();
                
                // trigger the mini-viz.
                if(bin_data.hasOwnProperty(key)) {
                    target = bin_data[key].length;
                } else {
                    target = 0;
                }
                
                (function(vizbin, target) {
                    vizbin.$miniviz = $(vizbin.miniviz);
                    vizbin.$minict = $(vizbin.miniviz_ct);
                    vizbin.current = parseInt(vizbin.$minict.text(), 10);
                    
                    vizbin.updates = vizbin.current - target;
                    vizbin.tmp = vizbin.current;
                    
                    vizbin.loop = setInterval(function() {
                        if(vizbin.updates > 0) {
                            vizbin.tmp -= 1;
                            vizbin.$miniviz.children().last().remove();
                            vizbin.$minict.text(vizbin.tmp);
                            vizbin.updates--;
                        } else if (vizbin.updates < 0) {
                            vizbin.tmp += 1;
                            vizbin.$miniviz.append('<div class="dot"></div>');
                            vizbin.$minict.text(vizbin.tmp);
                            vizbin.updates++;
                        } else {
                            clearInterval(vizbin.loop);
                        }
                    }, 25);
                })(vizbin, target);
            });
            $data.bin_data = bin_data;
        }
        
        ////////////
        // Update //
        ////////////
        
        function update_viz(initial, animate, callback, text_update) {
            if(_(callback).isUndefined()) { callback = function() {}; }
            if(_(text_update).isUndefined()) { text_update = function() {}; }
            
            // set up the default viz
            viz = get_viz();
            
            if(_(animate).isUndefined()) {
                animate = { in: 'fadeIn', out: 'fadeOut' };
            }
            
            $(".question-container").animo({ animation: animate.out, duration: 0.2 }, function() {
                $this.find('.question').text(viz.question);
                $this.find('.explanation').text(viz.explanation);
                if(viz.directed_to) {
                    $this.find('.directed_to').text(viz.directed_to.toUpperCase()+":");
                } else {
                    $this.find('.directed_to').text("");
                }
                text_update();
                $(".question-container").animo({ animation: animate.in, duration: 0.6 }, callback);
                $data.post_update();
            });
            
            // set up bins for initial viz
            bins = {}; bin_keys = [];
            _(viz.bins).each(function(value, key, list) {
                // this seeds the bin variable
                // with instanced counterparts in the DOM
                value.key = key;
                bin_keys.push(key);
                
                if(initial) {
                    $this.find($data.bin_holder).append(
                        bin_template(value)
                    );
                }
                
                value.wrapper = $this.find("#"+key+"-wrapper");
                value.bin = value.wrapper.find(".bin");
                
                value.miniviz = value.wrapper.find(".miniviz");
                value.miniviz_ct = value.wrapper.find(".miniviz-ct");
                
                if(initial) {
                    value.isotope = value.bin.isotope($data.isotope);
                    bins[key] = $(value.bin);
                } else {
                    value.isotope = $data.bins[key];
                }
            });
            if(initial) { $data.bins = bins; $data.bin_keys = bin_keys; }
        }
        
        //////////
        // Init //
        //////////
        
        init = _.once(function() {
            var bins;
            
            $this.data($.extend( {}, $.fn.checkup.defaults, options ));
            $data = $this.data();
            
            bin_template = _.template($data.bin_template);
            box_template = _.template($data.box_template);
            
            // set up viz
            update_viz(true);
            
            // insert data first time
            $.getJSON($data.json, function(d) {
                _(d.assignments).each(function(value, key, list) {
                    value.key = key;
                });
                
                $data.data = d;
                
                _($data.data.assignments).each(function(assignment, index, list) {
                    assignment.box_html = box_template(assignment);
                });
                
                render();
            });
        });
        
        switch_viz = function(i, animate, callback, text_update) {
            var data;
            data = $data.data;
            
            if(_(callback).isUndefined()) { callback = function() {}; }
            if(_(text_update).isUndefined()) { text_update = function() {}; }
            
            if($data['active-viz'] === i) { return; }
            $data['active-viz'] = i;
            // animate visualizaiton switch
            $("#bin-holder").animo({ animation: 'fadeOutUp', duration: 0.1, keep: true }, function() {
                update_viz(false, animate, function() {
                    $("#bin-holder").animo({ animation: 'fadeInDown', duration: 0.6, keep: true }, function() {
                        $("#bin-holder").animo("cleanse");
                        callback();
                    });
                    render();
                }, text_update);
            });
        };
        
        // Go!
        init();
        
        $data.fns = {
            switch_viz: switch_viz,
            data: get_data,
            viz: get_viz
        };
        return $data.fns;
    };
    
    $.fn.checkup.defaults = {
        'active-viz': 0,
        post_update: function() {},
        'animate': { in: 'fadeIn', out: 'fadeOut' },
        'isotope': {
            itemSelector: '.item',
            layoutMode: 'fitRows',
            containerStyle: { position: 'relative', overflow: 'show' }, // temporary bugfix, fix for v2
            getSortData : {
                status : function ($elem) {
                  return $elem.attr('id').split("-")[0] + $elem.find(".last_name").text();
                }
            },
            sortBy: 'status'
        }
    };
 
}( jQuery ));
