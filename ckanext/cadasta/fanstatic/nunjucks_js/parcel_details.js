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

            parcel_history_details.forEach(function(parcel) {
                var date_modified = new Date(parcel.date_modified);
                var month = date_modified.getMonth();
                var day = date_modified.getDay();
                var year = date_modified.getFullYear();
                var date_modified_formatted = month + "/" + day + "/" + year;
                parcel.date_modified = date_modified_formatted;

                var date_created = new Date(parcel.time_created);
                var month = date_created.getMonth();
                var day = date_created.getDay();
                var year = date_created.getFullYear();
                var date_created_formatted = month + "/" + day + "/" + year;
                parcel.time_created = date_created_formatted;

                var time_updated = new Date(parcel.time_updated);
                var month = time_updated.getMonth();
                var day = time_updated.getDay();
                var year = time_updated.getFullYear();
                var time_updated_formatted = month + "/" + day + "/" + year;
                parcel.time_updated = time_updated_formatted;

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
