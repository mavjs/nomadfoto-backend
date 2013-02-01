(function ($) {
    // function to append to a certain node in html
    
    function populate_gallery(node, images) {
        $.each(images, function (idx, image) {
            //node.append('<li style="display: block;"><div><img src="' + image.url + '" /></div></li>');
            node.append('<li><a href="#" class="thumbnail"><img src="' + image.url + '" /></a></li>');
        });
    }

    // function to GetForms.
    function GetForms(jobs) {
        $.get('/resources/json/' + $('.basket-action').val() + 'form.html', function (data) {
            $('.basket-options-form').html(data);
        });
    }
    // function to ShowForms.
    function ShowForms() {
        $('.basket-action').change(function (ev) {
            var action = $(ev.target).val();
            $.get('/resources/json/' + action + 'form.html', function (data) {
                $('.basket-options-form').html(data);
            });
        });
    }

    function ShowMain() {
        $.get('/resources/json/jobsection.html', function (data) {
            var jobs = data;
            $('.orderbaskets').append(jobs);
        });
    }
     // on document ready load the functions
     $(document).ready(function() {
            GetForms();
            ShowForms();
            $('.thumbnails li').draggable({ 
                helper: "clone",
                revert: "invalid"
            });
            $('.droppable').droppable({
                activeClass: "ui-state-default",
                hoverClass: "ui-state-hover",
                drop: function(event, ui) {
                    $( this ).find( ".placeholder" ).remove();
                    $( this ).append('<li>' + ui.draggable.html() + '</li>');
                }
            });
        });
        $('#joborder').click(function() {
            ShowMain();
        });
     });
})(jQuery);
