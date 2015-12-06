var express = require('express');
// var client = require('./client');
var utils = require('../utils');
var router = express.Router();
var plotly = require('plotly')("krkini16", "blzpptw3c0")
//Client for DB
var net = require('net');



candidateList = ["Hillary Clinton", "Carly Fiorina", "Bernie Sanders", "Marco Rubio", "Donald Trump", "Ted Cruz", "Ben Carson", "Rand Paul"];

router.get('/', function(req, res, next) {
  res.render('index', { 
  		title: 'Express',
  		candidates : candidateList
  	});
});

router.get('/select/:query', function(req, res, next) {
  q = req.params.query;
  // client.send_query(q, function(data){
  // 	  console.log(res);
  //     utils.sendSuccessResponse(res,{data: data});
  // })
	var client = new net.Socket();
	client.setNoDelay(); 
	client.connect(8000, '127.0.0.1', function() {
		console.log('Connected');
		//Hardcoded tweet to examine workflow
		//send_query('3#1448082159999|Trump;');
	});

	client.on('close', function() {
		console.log('Connection closed');
	});

	client.write(q, function(response){
		client.on('data', function(data) {
			console.log("Response data");
			console.log(data.toString());
			utils.sendSuccessResponse(res, {data: data.toString()});
			client.destroy();
		});
	});

})

module.exports = router;