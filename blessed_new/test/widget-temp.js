var blessed = require('../')
  , screen
  , fs = require('fs');

screen = blessed.screen({
  autoPadding: false,
  fullUnicode: true,
  warnings: true
});

var dir = '/home/pi/masonInPython/epaper_clock/';

var tempfile = dir+'home_air.json';

var weatherfile = dir+'weather.json';

var linuxtempfile = dir+'linux_temp.json';

var tempresult=JSON.parse(fs.readFileSync( tempfile));

var weatherresult=JSON.parse(fs.readFileSync( weatherfile));

var linuxtempresult=JSON.parse(fs.readFileSync( linuxtempfile));

var table = blessed.table({

  top: 'center',
  left: 'center',
  data: null,
  border: 'line',
  align: 'center',
  tags: true,
  width: 'shrink',
  style: {
    border: {
      fg: 'red'
    },
    header: {
      fg: 'blue',
      bold: true
    },
    cell: {
      fg: 'magenta'
    }
  }
});

function updateTime() {
  var pos = 0
    , d = new Date
    , im = '上午'
    , time
    , h
    , m
    , s;

  h = d.getHours();
  if (h >= 12) {
    im = '下午';
  }
  if (h > 12) {
    h -= 12;
  }
  if (h === 0) h = 12;
  if (h < 10) {
    h = '0' + h;
  }

  m = d.getMinutes();
  if (m < 10) {
    m = '0' + m;
  }

  s = d.getSeconds();
  if (s < 10) {
    s = '0' + s;
  }

  time =  im + h + ':' + m;

  return time;
}

function getLocalTime(nS) {     
   return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');     
}  

  var data1 = [
    [ '服务器CPU温度:'+linuxtempresult.cpu_temp,'服务器GPU温度:'+linuxtempresult.gpu_temp],
    [ weatherresult.city_name,  updateTime() ],
    [ '家里温度', tempresult.temp+'℃' ],
    [ '家里湿度', tempresult.humidity+'%' ],
    [ '当前室外温度', weatherresult.current_temp+'℃' ],
    [ '当前室外湿度', weatherresult.current_humidity+'%' ],
    [ '今天最低温度',   weatherresult.today_temp_low+'℃' ],
  ];

  if(weatherresult.today_temp_hig){
    data1.push([ '今天最高温度',    weatherresult.today_temp_hig+'℃' ]);
    data1.push([ '今天天气',   weatherresult.today_weather ]);
    data1.push([ '明天最低温度',    weatherresult.tomorrow_temp_low+'℃' ]);
    data1.push([ '明天最高温度',    weatherresult.tomorrow_temp_hig+'℃' ]);
    data1.push([ '明天天气',    weatherresult.tomorrow_weather ]);
  }else{
    data1.push([ '今天天气',   weatherresult.today_weather ]);
    data1.push([ '明天最低温度',    weatherresult.tomorrow_temp_low+'℃' ]);
    data1.push([ '明天最高温度',    weatherresult.tomorrow_temp_hig+'℃' ]);
    data1.push([ '明天天气',    weatherresult.tomorrow_weather ]);
  }

  data1.push(['最后更新时间',getLocalTime(tempresult.update)]);

screen.key('q', function() {
  return screen.destroy();
});

table.setData(data1);
screen.append(table);
screen.render();

setInterval(function() {

  var dir = '/home/pi/masonInPython/epaper_clock/';

  var tempfile = dir+'home_air.json';

  var weatherfile = dir+'weather.json';

  var linuxtempfile = dir+'linux_temp.json';

  var tempresult=JSON.parse(fs.readFileSync( tempfile));

  var weatherresult=JSON.parse(fs.readFileSync( weatherfile));

  var linuxtempresult=JSON.parse(fs.readFileSync( linuxtempfile));

  var data2 = [
    [ '服务器CPU温度:'+linuxtempresult.cpu_temp,'服务器GPU温度:'+linuxtempresult.gpu_temp],
    [ weatherresult.city_name,  updateTime() ],
    [ '家里温度', tempresult.temp+'℃' ],
    [ '家里湿度', tempresult.humidity+'%' ],
    [ '当前室外温度', weatherresult.current_temp+'℃' ],
    [ '当前室外湿度', weatherresult.current_humidity+'%' ],
    [ '今天最低温度',   weatherresult.today_temp_low+'℃' ],
  ];

  if(weatherresult.today_temp_hig){
    data2.push([ '今天最高温度',    weatherresult.today_temp_hig+'℃' ]);
    data2.push([ '今天天气',   weatherresult.today_weather ]);
    data2.push([ '明天最低温度',    weatherresult.tomorrow_temp_low+'℃' ]);
    data2.push([ '明天最高温度',    weatherresult.tomorrow_temp_hig+'℃' ]);
    data2.push([ '明天天气',    weatherresult.tomorrow_weather ]);
  }else{
    data2.push([ '今天天气',   weatherresult.today_weather ]);
    data2.push([ '明天最低温度',    weatherresult.tomorrow_temp_low+'℃' ]);
    data2.push([ '明天最高温度',    weatherresult.tomorrow_temp_hig+'℃' ]);
    data2.push([ '明天天气',    weatherresult.tomorrow_weather ]);
  }

  data2.push(['最后更新时间',getLocalTime(tempresult.update)]);

  table.setData(data2);
  screen.render();
}, 3000);
