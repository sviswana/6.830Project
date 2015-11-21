var plotly = require('plotly')("krkini16", "blzpptw3c0")

//Client for DB
var net = require('net');

var client = new net.Socket();
client.connect(8000, '127.0.0.1', function() {
	console.log('Connected');
	//Hardcoded tweet to examine workflow
	client.write('3#1448082159999|Trump;');
});

//This is a listener for whenever we receive data
client.on('data', function(data) {
	console.log('Received: ' + data);
	// client.destroy(); // kill client after server's response: SHOULD be uncommented but sends an automatic message to the server which can't be parsed yet
});

//This is for when we send a close operation
//Idk if we ever will until we want to be clean, but
//in that circumstance, we should also neatly close the
//Server port
client.on('close', function() {
	console.log('Connection closed');
});

//Server for WebApp
var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Hello World!'); //Insert webpage here
});

var server = app.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log('Basic app listening at http://%s:%s', host, port);
});