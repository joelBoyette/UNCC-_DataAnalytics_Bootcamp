// Creating map object
var myMap = L.map("map", {
  center: [0, 0],
  zoom: 2
});

// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 11,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);

function magnitudeColor(magnitude) {
    switch (true) {
    case (magnitude>= 4.0 && magnitude < 5.0):
      return "green";
    case magnitude >= 5.0 && magnitude < 6.0:
      return "yellow";
    case magnitude >= 6.0 && magnitude < 7.0:
      return "orange";  
    case magnitude >= 7.0 && magnitude < 8.0:
      return "red";    
    default:
      return "white";
  }
}



url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson'

d3.json(url, function(response) {

    var features = response.features;

    for (var i = 0 ; i < features.length; i++){

      var lng = features[i].geometry.coordinates[0];
      var lat = features[i].geometry.coordinates[1];
            
      var magnitude = features[i].properties.mag;
      var place = features[i].properties.place;

      console.log(magnitude);

      L.circle([lat,lng], {
          fillOpacity: 0.75,
          color: magnitudeColor(magnitude),
          fillColor: magnitudeColor(magnitude),
          radius: magnitude * 10000
      }).bindPopup("<h1>" + place + "</h1> <hr> <h3>Magnitude: " + magnitude + "</h3>")
        .addTo(myMap);

    }

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

      var div = L.DomUtil.create('div', 'info legend'),
      
      magnitudeLegend = [4,5,6,7,8],
      
      // loop through our density intervals and generate a label with a colored square for each interval
      for (var i = 0; i < magnitudeLegend.length; i++) {
          div.innerHTML +=
              '<i style="background:' + magnitudeColor(magnitudeLegend[i]) + '"></i> ' +
              magnitudeLegend[i] + (magnitudeLegend[i + 1] ?'&ndash;' + magnitudeLegend[i + 1] + '<br>' : '+');
      } 

      return div;
    };

    legend.addTo(myMap);

})
  