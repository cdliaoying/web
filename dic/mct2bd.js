
//以下两句话为创建地图
var map = new BMap.Map("container");
    map.centerAndZoom(new BMap.Point(108.318421,22.800617), 15);

function mctGeo()
{
    map.clearOverlays();
    document.getElementById("panel").innerHTML = "";

    var mctXX = document.getElementById("mctX").value;
    var mctYY = document.getElementById("mctY").value;
    var mctXY = new BMap.Pixel(mctXX,mctYY);

    var projection2 = map.getMapType().getProjection();
    var LngLat = projection2.pointToLngLat(mctXY);

    document.getElementById("pointX").innerHTML = "经纬度lng: " + LngLat.lng;
    document.getElementById("pointY").innerHTML = "经纬度lat: " + LngLat.lat;
}


