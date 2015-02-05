var map;
var lines = [];
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
  lines[lines.length] = new google.maps.Polyline({
    path: flightPlanCoordinates,
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2,
    icons: [{
      icon: lineSymbol,
      offset: '0%'
    }],
  });
  lines[lines.length - 1].setMap(map);
  lines[lines.length - 1].dis = 0;
  lines[lines.length - 1].data = obj;

  distanceToPercentage(lines[lines.length - 1].data, 22);
}

function start_updateloop(){
  updateLoop();
}

function updateLoop() {
    var count = 0;
    window.setInterval(function() {
      /*count = (count + 1) % 200;

      var icons = flightPath.get('icons');
      icons[0].offset = (count / 2) + '%';
      flightPath.set('icons', icons);*/
      for (var i = lines.length - 1; i >= 0; i--) {
        lines[i].dis += lines[i].data.speed ;
        var icons = lines[i].get('icons');
        icons[0].offset = distanceToPercentage(lines[i].data, lines[i].dis) + '%';
        lines[i].set('icons', icons);
      }
  }, 1000);
}

function distanceToPercentage(dataObj, curr_dis){
  var dis = google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(dataObj.begin_lat, dataObj.begin_long), new google.maps.LatLng(dataObj.end_lat, dataObj.end_long));
  var percent = 100 / dis * curr_dis;
  return percent;
}

google.maps.event.addDomListener(window, 'load', initialize);