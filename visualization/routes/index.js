var express = require('express');
var client = require('./client');
var utils = require('../utils');
var router = express.Router();

router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/select/:query', function(req, res, next) {
  q = req.params.query;
  client.send_query(q, function(data){
      utils.sendSuccessResponse(res,{data: data});
  })
})

module.exports = router;