$(document).ready(function() {


    $.router.add("/project/:project_id/parcels", function(data) {
        console.log(data.item);
    });

    function onFormChanged(){

    }

    $('#FilterForm').submit(function (e) {

        var data = {};
        $("#FilterForm").serializeArray().map(function(x){data[x.name] = x.value;});


        // This will change the url to http://www.foo.com/items/mycoolitem and set the title to
        // "My cool item" without reloading the page. If using hashes instead, it will use the url
        // http://www.foo.com/#!items/mycoolitem.
        // If a route has been set that matches it, it will be triggered.



        $.router.go("?foo=bar");

        e.preventDefault();
    });

    //Get Querystring args
    function getQuerystringArgs(){
        var queryParams = $.getQueryParameters();

    }


    function getFormArgs(){

    }



    function callAPI(options) {

        //Given the options, call the API with querystring args
        //Hit API and get back response
        var url = "http://54.69.121.180:3000/show_parcels_list";

        var args = [];
        for(var key in Object.keys(options)){
            args.push(key + "=" + options[key]);
        }

        if(args.length > 0){
            url += "?" + args.join("&");
        }

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



})
