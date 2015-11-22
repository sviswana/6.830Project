var express = require('express');
var plotly = require('plotly')("krkini16", "blzpptw3c0")
//Client for DB
var net = require('net');

var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

var client = new net.Socket();
client.connect(8000, '127.0.0.1', function() {
	console.log('Connected');
	//Hardcoded tweet to examine workflow
	//client.write('3#1448082159999|Trump;');

	var data = [
  {
    x: ["2013-10-04 22:23:00", "2013-11-04 22:23:00", "2013-12-04 22:23:00"],
    y: [1, 3, 6],
    type: "scatter"
  }
];
var graphOptions = {filename: "date-axes", fileopt: "overwrite"};
plotly.plot(data, graphOptions, function (err, msg) {
    console.log(msg);
});

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

module.exports = router;
