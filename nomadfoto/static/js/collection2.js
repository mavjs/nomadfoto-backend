(function ($) {
    // function to append to a certain node in html
    populate_gallery = function (node, images) {
        $.each(images, function (idx, image) {
            //node.append('<li style="display: block;"><div><img src="' + image.url + '" /></div></li>');
            node.append('<li><a href="#boxeffect" id="boxeffect"><img src="' + image.url + '" /></a></li>');
        });
    };
    // function to GetForms.
    GetForms = function () {
        $.get('json/' + $('.basket-action').val() + 'form.html', function (data) {
            $('.basket-options-form').html(data);
        });
    };
    // function to ShowForms.
    ShowForms = function () {
        $('.basket-action').change(function (ev) {
            var action = $(ev.target).val();
            $.get('json/' + action + 'form.html', function (data) {
                $('.basket-options-form').html(data);
            });
        });
    }
    var jobs = function () {
                var count = 0;
                $.get('json/jobsection.html', function (data) {
                    var startsec = '<section class="slide" id="jobs-'+count+'">\n';
                    var endsec = '</section>\n';
                    $('.JobSection').append(startsec + data + endsec);
                    GetForms();
                    ShowForms();
                    $.getJSON('json/images.json', {}, function (data) {
                          populate_gallery($('.thumbnails'), data)
                    });
                $('#joborder').click(function() {
                    jobs();
                    count = count + 1;
                });
                $('#boxeffect').click(function() {
                    alert('Hello!');
                });
              });
            }
     // on document ready load the functions
     $(document).ready(function() {
            jobs();
            var mySlider = new Swipe(document.getElementById('slider'));
            $('#prev').click(function () {
                mySlider.prev();
            });
            $('#next').click(function () {
                mySlider.next();
            });
     });
})(jQuery);
