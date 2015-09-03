$(document).ready(function() {

    //Hit API and get back response
    var url = "http://54.69.121.180:3000/show_activity";

    $.ajax(url).done(function (response) {
        //success
            nunjucks.configure('/nunjucks_snippets', {autoescape: true});
            var res = nunjucks.render('activity_list.html', response);

             $("#nunjuck-activity-list").html(res);
    })
    .fail(function () {
        //err
    })
    .always(function () {
        //no matter what
    });



})
