$(document).ready(function() {

        //Given the options, call the API with querystring args
        //Hit API and get back response
        var url = "http://54.69.121.180:3000/show_parcels_list";

        $.ajax(url).done(function (response) {
            //success
            nunjucks.configure('/nunjucks_snippets', {autoescape: true});
            var res = nunjucks.render('parcel_list.html', response);

             $("#nunjuck-parcel-list").append(res);
        })
        .fail(function () {
            //err
        })
        .always(function () {
            //no matter what
        });



});
