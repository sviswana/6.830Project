var express = require('express');
var plotly = require('plotly')("krkini16", "blzpptw3c0")
//Client for DB
var net = require('net');

var client = new net.Socket();
client.setNoDelay(); 
var ans = '';
client.connect(8000, '127.0.0.1', function() {
	console.log('Connected');
	//Hardcoded tweet to examine workflow
	//send_query('3#1448082159999|Trump;');
});



//This is a listener for whenever we receive data


//This is for when we send a close operation
//Idk if we ever will until we want to be clean, but
//in that circumstance, we should also neatly close the
//Server port
client.on('close', function() {
	console.log('Connection closed');
});


//module.exports = router;
function send_query(query, callback){ 

	var send = function() {
		client.write(query, function(response){
			client.on('data', function(data) {
			//console.log('Received: ' + data);
	// client.destroy(); // kill client after server's response: SHOULD be uncommented but sends an automatic message to the server which can't be parsed yet
				callback(data.toString());
			});
		//client.destroy(); 
		})
	}
};

//module.exports = send_query;
module.exports= {
	send_query: send_query,
};