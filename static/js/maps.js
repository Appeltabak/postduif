var map; // The global map object
var lines = []; // all lines to be updated.
// object which is to be drawn on the fligt line.
var lineSymbol = {
  // duif svg
  path: 'm47,572c-34,-35 -34,-42 -1,-42c26,0 26,-1 18,-42c-5,-24 -9,-73 -9,-110c1,-81 15,-105 101,-164c89,-61 84,-114 -10,-114c-41,-1 -41,-1 -16,-15c14,-8 21,-15 15,-15c-5,-1 3,-7 19,-14c19,-9 41,-10 64,-5c19,4 41,5 48,2c8,-3 14,0 14,6c0,6 -4,11 -10,11c-15,0 -12,26 5,40c8,7 15,23 15,36c0,13 7,25 18,28c49,14 156,17 226,6c81,-14 111,-8 57,11c-24,9 -30,15 -26,30c7,20 10,18 -93,39c-37,7 -80,28 -145,71c-131,88 -146,103 -153,163c-5,36 -15,59 -35,78c-35,36 -68,35 -102,0z',
  scale: 0.04,
  fillColor: 'green',
  fillOpacity: 1,
  strokeOpacity: 0,
  strokeWeight: 1,
  rotation: -60,
  anchor: new google.maps.Point(150, 350)
};
/**
 * builds new map object.
 */
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

/**
 * draws a new fligt line to the map.
 * @map  the map object
 * @obj  the data object from the database containing information about the flight.
 */
function draw_flight(map, obj){
  var flightPlanCoordinates = [
    new google.maps.LatLng(JSON.parse(obj.begin).lat, JSON.parse(obj.begin).lng),
    new google.maps.LatLng(JSON.parse(obj.end).lat, JSON.parse(obj.end).lng)
  ];
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

/**
 * start new updateloop.
 */
function start_updateloop(){
  updateLoop();
}

/**
 * the updateloop. updates every second.
 */
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

/**
 * calculates the percentage at which the symbol should be drawn.
 * @dataObj  the data object from the database.
 * @curr_dis the current distance of the symbol/duif.
 * @return the percentage
 */
function distanceToPercentage(dataObj, curr_dis){
  var dis = google.maps.geometry.spherical.computeDistanceBetween(new google.maps.LatLng(JSON.parse(dataObj.begin).lat, JSON.parse(dataObj.begin).lng), new google.maps.LatLng(JSON.parse(dataObj.end).lat, JSON.parse(dataObj.end).lng));
  var percent = 100 / dis * curr_dis;
  return percent;
}

// initialize the map.
google.maps.event.addDomListener(window, 'load', initialize);