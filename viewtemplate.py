<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>HDB Singapore</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

// This example creates a simple polygon representing the Bermuda Triangle.

function buildpolygon(map,coords) {
 // Define the LatLng coordinates for the polygon's path.
  var triangleCoords = [
    {lat: coords[0], lng: coords[1]},
    {lat: coords[0], lng: coords[3]},
    {lat: coords[2], lng: coords[3]},
    {lat: coords[2], lng: coords[1]},
    {lat: coords[0], lng: coords[1]}
  ];

  // Construct the polygon.
  var bermudaTriangle = new google.maps.Polygon({
    paths: triangleCoords,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35
  });
  bermudaTriangle.setMap(map);
}

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: {lat: 1.352083, lng: 103.819836},
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  var coordss = [ [1.3719565, 103.9001748, 1.3713879, 103.8995004],
                  [1.373497, 103.849476, 1.37327, 103.848611],
                  [1.3663186, 103.8506205, 1.366194, 103.8495851] ];

  for (var i = 0; i < coordss.length; i++) {
		      buildpolygon(map, coordss[i]);
  }
}

    </script>
    <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBU64AzWbUE14EhZ9TITH4j5PiCY1iGemc&signed_in=true&callback=initMap"></script>
  </body>
</html>
