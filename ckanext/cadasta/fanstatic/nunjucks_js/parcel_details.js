$(document).ready(function() {

    //Hit API and get back response
    var url = "http://54.69.121.180:3000/parcels/1/details";
    //TODO do we need to get the dynamic parcel number from the url?

    $.ajax(url).done(function (response) {
        //success
            nunjucks.configure('/nunjucks_snippets', {autoescape: true});

            var parcel_details = response.features[0].properties;
            var res = nunjucks.render('parcel_details.html', {parcel_details:parcel_details});
             $("#nunjuck-parcel-details-list").html(res);


            var relationships = response.features[0].properties.relationships;
            var res_relationships = nunjucks.render('parcel_details_relationships.html', {relationships:relationships} );
             $("#nunjuck-parcel-details-relationships").html(res_relationships);

            var parcel_history_details = response.features[0].properties.parcel_history;

            var format_date = function(date) {
                var date_object = new Date(date);
                var month = date_object.getMonth();
                var day = date_object.getDay();
                var year = date_object.getFullYear();
                var date_object_formatted = month + "/" + day + "/" + year;

                return date_object_formatted;
            }

            parcel_history_details.forEach(function(parcel) {

                parcel.date_modified = format_date(parcel.date_modified);
                parcel.time_created = format_date(parcel.time_created);
                parcel.time_updated = format_date(parcel.time_updated);

            })


            var res_parcel_history = nunjucks.render('parcel_details_history.html', {parcel_history_details:parcel_history_details});
             $("#nunjuck-parcel-details-history").html(res_parcel_history);
    })
    .fail(function () {
        //err
    })
    .always(function () {
        //no matter what
    });



})
