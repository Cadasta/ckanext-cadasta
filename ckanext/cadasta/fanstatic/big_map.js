
L.mapbox.accessToken = 'pk.eyJ1Ijoic2JpbmRtYW4iLCJhIjoiaENWQnlrVSJ9.0DQyCLWgA0j8yBpmvt3bGA';






$(document).ready(function() {

    var map = L.mapbox.map('big_map', 'mapbox.streets');

    var featureGroup, parcelsFeatureGroup;
    var parcel_layer, drawControl;

    map.on("load", function () {
        featureGroup = L.featureGroup().addTo(map);
        parcelsFeatureGroup = L.featureGroup().addTo(map);

        featureGroup.on("load", function () {
            displayParcels(map);
        })

        drawControl = new L.Control.Draw({
            edit: {
                featureGroup: featureGroup
            },
            draw: {
                polyline: false,
                circle: false, // Turns off this drawing tool
                rectangle: false,
                marker: false
            }
        }).addTo(map);
    })


    map.on('draw:created', function (e) {
        var layer = e.layer;
        //make sure there is only one geometry
        if (featureGroup && featureGroup.getLayers().length !== 0) {
            featureGroup.clearLayers();
        }

        featureGroup.addLayer(layer);
        addParcel();
    });


    function addParcel() {
        var json = featureGroup.toGeoJSON();
        var elem = document.getElementById("parcel_geom");
        elem.value = json.features[0].geometry.coordinates[0];
    }


    function displayParcels(map) {
//    converts string data into a geojson object that can be mapped

        var parcelCollection = $('#data').data();
        var popupURL = $('#popup_url').data().obj;

        var parcel_string = JSON.stringify(parcelCollection);
        parcel_string = parcel_string.replace('{"obj":', '');
        parcel_string = parcel_string.replace('}}]}}', '}}]}');

        var parcel_geoJSON = JSON.parse(parcel_string);

        parcel_layer = L.geoJson(parcel_geoJSON, {
            style: function (feature) {
                return {color: 'green'};
            },
            onEachFeature: function (feature, layer) {
                layer.bindPopup("<a href=" + popupURL + layer.feature.name + ">See Parcel Details</a>");
            }
        });

        parcel_layer.on("click", function (e) {
            e.layer.options.color = "black";
            e.layer.options.fill = "black";
        });

        parcel_layer.addTo(parcelsFeatureGroup);
        map.fitBounds(parcelsFeatureGroup.getBounds());

    }

})






