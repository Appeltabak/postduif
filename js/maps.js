var map;
function initialize() {
  var mapOptions = {
    center: { lat: 53.1, lng: 6.25},
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.HYBRID,
    disableDefaultUI: true
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);
}
function draw_flight(map, obj){
  var flightPlanCoordinates = [
    new google.maps.LatLng(obj.begin_lat, obj.begin_long),
    new google.maps.LatLng(obj.end_lat, obj.end_long)
  ];
  var lineSymbol = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 8,
    strokeColor: '#393'
  };
  var flightPath = new google.maps.Polyline({
    path: flightPlanCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2,
    icons: [{
      icon: lineSymbol,
      offset: '100%'
    }],
  });
  flightPath.setMap(map);
}
google.maps.event.addDomListener(window, 'load', initialize); 