
L.mapbox.accessToken = 'pk.eyJ1Ijoic2JpbmRtYW4iLCJhIjoiaENWQnlrVSJ9.0DQyCLWgA0j8yBpmvt3bGA';

  var map = L.mapbox.map('small_map', 'mapbox.streets');

  var featureGroup = L.featureGroup().addTo(map);
  var parcelsFeatureGroup = L.featureGroup().addTo(map);

  var json = '';

  var parcel_layer;


  var drawControl = new L.Control.Draw({
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

  map.on('draw:created', function(e) {
    var layer = e.layer;
    //make sure there is only one geometry
    if(featureGroup && featureGroup.getLayers().length!==0){
      featureGroup.clearLayers();
    }

    featureGroup.addLayer(layer);
    addParcel();
  });


function displayParcels (map) {
//    converts string data into a geojson object that can be mapped

    var parcelCollection = $('#small_map_data').data();
    var smallPopupURL = $('#small_popup_url').data().obj;

    var parcel_string = JSON.stringify(parcelCollection);
    parcel_string = parcel_string.replace('{"obj":', '');
    parcel_string = parcel_string.replace('}}]}}', '}}]}');

    var parcel_geoJSON = JSON.parse(parcel_string);

    parcel_layer = L.geoJson(parcel_geoJSON, {
        style: function (feature) {
        return {color: 'green'};
        },
        onEachFeature: function (feature, layer) {
            layer.bindPopup("<a href="+ smallPopupURL + layer.feature.name + ">See Parcel Details</a>");
        }
    });

    parcel_layer.addTo(parcelsFeatureGroup);
    map.fitBounds(parcelsFeatureGroup.getBounds());

}

//move this to the jquery, on document load run this function
displayParcels (map);


function addParcel() {
    json = featureGroup.toGeoJSON();

    var elem = document.getElementById("parcel_geom");
    elem.value = json.features[0].geometry.coordinates[0];
}



parcel_layer.on("click", function(e) {
    e.layer.options.color="black";
    e.layer.options.fill="black";
});

