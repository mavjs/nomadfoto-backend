            (function ($) {
                var populate_jobs = function (node, jobs) {
                $.each(jobs, function (idx, job) {
                    node.append('<li id="' + job.status + '" class="alert alert-' + job.status + '"><a href="' + job.url + '">' + job.title + '</a><br />Client Name: ' + job.client + '<br />Job Ordered Date: ' + job.start + '<br />Job End Date: ' + job.end + '</li>');
                })
            }
                var jobdone = function() {
                    $.getJSON('json/jobsuccess.json', {}, function (data) {
                        populate_jobs($('#jobdone'), data)
                    });
                }
                var jobpend = function() {
                    $.getJSON('json/joberror.json', {}, function (data) {
                        populate_jobs($('#jobpend'), data)
                    });
                }
                $(document).ready(function () {
                    jobdone();
                    jobpend();
                    /* $('#jobdone').toggle(function(event) {
                            $("li[id*='success']").each(function () {
                                $(this).hide('slow');
                            });
                        }, function (event) {
                                $("li[id*='success']").each(function () {
                                    $(this).show('slow');
                                });
                        });
                    $('#jobundone').toggle(function(event) {
                            $("li[id*='error']").each(function () {
                                $(this).hide('slow');
                            });
                        }, function (event) {
                                $("li[id*='error']").each(function () {
                                    $(this).show('slow');
                                });
                        });*/
                    });
            })(jQuery);

