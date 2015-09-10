$(document).ready(function() {

    var format_date = function(date) {
        var date_object = new Date(date);
        var month = date_object.getMonth();
        var day = date_object.getDay();
        var year = date_object.getFullYear();
        var date_object_formatted = month + "/" + day + "/" + year;

        return date_object_formatted;
    }

    //Hit API and get back response
    var url = "http://54.69.121.180:3000/parcels/1/details";
    //TODO do we need to get the dynamic parcel number from the url?

    $.ajax(url).done(function (response) {
        //success
            nunjucks.configure('/nunjucks_snippets', {autoescape: true});

            //parcel details table
            var parcel_details = response.features[0].properties;

            parcel_details.time_created = format_date(parcel_details.time_created);
            parcel_details.time_updated = format_date(parcel_details.time_updated);


            var res = nunjucks.render('parcel_details.html', {parcel_details:parcel_details});
             $("#nunjuck-parcel-details-list").html(res);

            //parcel details relationships table
            var parcel_relationships = response.features[0].properties.relationships;

            parcel_relationships.forEach(function(parcel_relationship) {
                parcel_relationship.time_created = format_date(parcel_relationship.time_created);
                parcel_relationship.time_updated = format_date(parcel_relationship.time_updated);
            })


            var res_relationships = nunjucks.render('parcel_details_relationships.html', {parcel_relationships:parcel_relationships} );
             $("#nunjuck-parcel-details-relationships").html(res_relationships);

            //parcel details history
            var parcel_history_details = response.features[0].properties.parcel_history;


            parcel_history_details.forEach(function(parcel) {
                parcel.date_modified = format_date(parcel.date_modified);
                parcel.time_created = format_date(parcel.time_created);
                parcel.time_updated = format_date(parcel.time_updated);
            })


            var res_parcel_history = nunjucks.render('parcel_details_history.html', {parcel_history_details:parcel_history_details});
             $("#nunjuck-parcel-details-history").html(res_parcel_history);


        //parcel resources
        // todo this needs to be updated
        var parcel_history_details = response.features[0].properties.parcel_history;
        //
        //
        //parcel_history_details.forEach(function(parcel) {
        //    parcel.date_modified = format_date(parcel.date_modified);
        //    parcel.time_created = format_date(parcel.time_created);
        //    parcel.time_updated = format_date(parcel.time_updated);
        //})
        //
        //
        var res_parcel_history = nunjucks.render('parcel_details_resources.html', {parcel_history_details:parcel_history_details});
        $("#nunjuck-parcel-details-resources").html(res_parcel_history);
    })
    .fail(function () {
        //err
    })
    .always(function () {
        //no matter what
    });



})
