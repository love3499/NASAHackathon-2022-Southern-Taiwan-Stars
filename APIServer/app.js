
class Map_Point {
    constructor(name, lat, lon, type, level, earthquake, rainfall, mudslide) {
        this.name = name;
        this.lat = lat;
        this.lon = lon;
        this.type = type;
        this.level = level;
        this.earthquake = earthquake;
        this.rainfall = rainfall;
        this.mudslide = mudslide;
    }
}
var https = require("https");
var Mudslide_Records = [];
Mudslide_Records.forEach(data => {
    data[2] = parseFloat(data[2]);
    data[3] = parseFloat(data[3]);
});
var Bridges = [];
var Rains = [];
var Earthquakes = [];
var rain_ok = false;
var earthquake_ok = false;

function Load_CSV(File_Name, split) {
    var data = require("fs").readFileSync(File_Name, "utf8");
    data = data.split(split);
    var result = [];
    for (var i = data.length - 1; i > 0; i--) {
        result.push(data[i].split(","));
    }
    return result;
}
function Load_Https_Data(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (response) => {
            let chunks_of_data = [];

            response.on('data', (fragments) => {
                chunks_of_data.push(fragments);
            });

            response.on('end', () => {
                let response_body = Buffer.concat(chunks_of_data);
                resolve(response_body.toString());
            });

            response.on('error', (error) => {
                reject(error);
            });
        });
    });
}
async function Load_Rain_Data() {
    try {
        let http_promise = Load_Https_Data('https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=CWB-87FD08D8-CE2D-478A-BA2F-52885C71A1B7&offset=0&format=JSON');
        let response_body = await http_promise;
        Rains = [];
        JSON.parse(response_body)['records']['location'].forEach(data => {
            Rains.push({
                lat: data['lat'],
                lon: data['lon'],
                time: data['time']['obsTime'],
                amount: data['weatherElement'][6]['elementValue']
            })
        });
        rain_ok = true;
        Initialize_Datas();
    }
    catch (error) {
        // Promise rejected
        console.log(error);
    }
}

async function Load_Earthquake_Data() {
    try {
        let http_promise = Load_Https_Data('https://opendata.cwb.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=CWB-87FD08D8-CE2D-478A-BA2F-52885C71A1B7&offset=0&format=JSON');
        let response_body = await http_promise;
        Earthquakes = [];
        JSON.parse(response_body)['records']['earthquake'].forEach(data => {
            Earthquakes.push({
                depth: data['earthquakeInfo']['depth']['value'],
                lat: data['earthquakeInfo']['epiCenter']['epiCenterLat']['value'],
                lon: data['earthquakeInfo']['epiCenter']['epiCenterLon']['value'],
                time: data['earthquakeInfo']['originTime'],
                magnitude: data['earthquakeInfo']['magnitude']['magnitudeValue']
            })
        });
        earthquake_ok = true;
        Initialize_Datas();
    }
    catch (error) {
        // Promise rejected
        console.log(error);
    }
}

Mudslide_Records = Load_CSV("Mudslide.csv", "\n");
Bridges = Load_CSV("Bridge.csv", "\r\n");
Load_Rain_Data();
Load_Earthquake_Data();

var express = require('express');
const { unwatchFile } = require("fs");
var app = express();

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});
//app.use('/public', express.static('public'));
function Get_Bridge_Point(name, lat, lon, type, color) {
    let rain_distance = 2147483647;
    let rain_data = 'N/A';
    let mudslide_distance = 2147483647;
    let mudslide_data = 'N/A';
    let earthquake_distance = 2147483647;
    let earthquake_data = 'N/A';
    Rains.forEach(data => {
        let dis = Math.sqrt(Math.pow(data.lat - lat, 2) + Math.pow(data.lon - lon, 2));
        if (dis < rain_distance) {
            rain_distance = dis;
            rain_data = data.amount + "mm (" + data.time + ")";
        }
    });
    Earthquakes.forEach(data => {
        let dis = Math.sqrt(Math.pow(data.lat - lat, 2) + Math.pow(data.lon - lon, 2));
        if (dis < earthquake_distance) {
            earthquake_distance = dis;
            earthquake_data = data.magnitude + ", " + data.depth + "km (" + data.time + ")";
        }
    });
    Mudslide_Records.forEach(data => {
        let dis = Math.sqrt(Math.pow(data[3] - lat, 2) + Math.pow(data[2] - lon, 2));
        if (dis < mudslide_distance) {
            mudslide_distance = dis;
            mudslide_data = "Alert (" + data[1] + ")";
        }
    });
    return new Map_Point(name, lat, lon, type, color, earthquake_data, rain_data, mudslide_data);
}

app.get('/', function (req, res) {
    var points = [];
    points.push(Get_Bridge_Point("新威大橋", 22.891489, 120.636051, "bridge", "orange"));
    points.push(Get_Bridge_Point("湖義路", 22.54134, 120.589545, "road", "red"));
    points.push(Get_Bridge_Point("大津橋", 22.88006, 120.647541, "bridge", "green"));
    points.push(Get_Bridge_Point("六龜大橋", 22.995832, 120.639753, "bridge", "green"));
    points.push(Get_Bridge_Point("高美大橋", 22.842108, 120.573683, "bridge", "orange"));
    points.push(Get_Bridge_Point("高樹大橋", 22.782504, 120.54526, "bridge", "green"));
    points.push(Get_Bridge_Point("屏156線", 22.070183, 120.774746, "road", "orange"));
    points.push(Get_Bridge_Point("溫泉路", 22.084287, 120.738354, "road", "green"));
    points.push(Get_Bridge_Point("新曆路", 22.044071, 120.734646, "road", "orange"));
    points.push(Get_Bridge_Point("獅子一巷", 22.232049, 120.681081, "road", "green"));
    Bridges.forEach(bridge => {
        points.push(Get_Bridge_Point(bridge[0], bridge[2], bridge[1], "bridge", "green"));
        //console.log(bridge);
    });
    res.render('map', { points: points, req: req });
})

app.get('/get_datas', function (req, res) {

    res.render('map', { points: points, req: req });
})
var points = [];
function Initialize_Datas() {
    if (!rain_ok)
        return;
    if (!earthquake_ok)
        return;
    points.push(Get_Bridge_Point("新威大橋", 22.891489, 120.636051, "bridge", "orange"));
    points.push(Get_Bridge_Point("湖義路", 22.54134, 120.589545, "road", "red"));
    points.push(Get_Bridge_Point("大津橋", 22.88006, 120.647541, "bridge", "green"));
    points.push(Get_Bridge_Point("六龜大橋", 22.995832, 120.639753, "bridge", "green"));
    points.push(Get_Bridge_Point("高美大橋", 22.842108, 120.573683, "bridge", "orange"));
    points.push(Get_Bridge_Point("高樹大橋", 22.782504, 120.54526, "bridge", "green"));
    points.push(Get_Bridge_Point("屏156線", 22.070183, 120.774746, "road", "orange"));
    points.push(Get_Bridge_Point("溫泉路", 22.084287, 120.738354, "road", "green"));
    points.push(Get_Bridge_Point("新曆路", 22.044071, 120.734646, "road", "orange"));
    points.push(Get_Bridge_Point("獅子一巷", 22.232049, 120.681081, "road", "green"));
    Bridges.forEach(bridge => {
        points.push(Get_Bridge_Point(bridge[0], bridge[2], bridge[1], "bridge", "green"));
    });
}
app.get('/get_points', function (req, res) {
    res.status(200).json({ "result": "success", "data": points });
});

var server = app.listen(8092, function () {

    var host = server.address().address;
    var port = server.address().port;

    console.log("啟動成功, Port: %s", port);

})