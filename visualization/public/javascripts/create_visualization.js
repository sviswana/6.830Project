$(document).ready(function(){
	// candidateList = ["Hillary Clinton",
	// "Carly Fiorina",
	// "Bernie Sanders",
	// "Marco Rubio", 
	// "Donald Trump", 
	// "Ted Cruz", 
	// "Ben Carson", 
	// "Rand Paul"];
	candidateList = [];


	timerange = [];
	interval = 300000;
	currentTime = 1448082159999; //TODO (change this) : new Date();
	DATA_SEPARATOR = "|";
	QTYPE_SEPARATOR = "#";
	QUERY_SEPARATOR = ";";
	traces = []

	for( var i = 0; i < 5; i++){
		timerange.push(currentTime - (i * interval));
	}
	endUNIX = timerange[0];
	startUNIX = timerange[timerange.length - 1];
	function initializeTraces(){
		traces = [];
	}

	function clearCandidates(){
		candidateList = [];
	}
	function addToTraces(traceList){
		// console.log(candidateList.length * ((endUNIX - startUNIX)/interval) + 1);
		traces = traces.concat(traceList);
		if(traces.length >= (candidateList.length * (((endUNIX - startUNIX)/interval) + 1 ) )){
			makeGraph(traces);
		}

	}

	function deserialize(fullquery){
		var query = fullquery.split(QUERY_SEPARATOR.toString())[0];
		var data = query.split(self.QTYPE_SEPARATOR)[1];
		var tupleList =  data.split(self.DATA_SEPARATOR);
		return tupleList
	}

	function detuple(tuple){
		return tuple.split(")")[0].split("(")[1].split(", ");
	}

	$('input[type=radio]').change(
		function(){
			clearCandidates();
			var id = $(this).attr('id');
			var index = candidateList.indexOf(id);
			var changed = false;
			if (this.checked) {
				if(index <= -1){
					candidateList.push(id);
					changed = true;
				}

			}
			else{
				if(index > -1){
					candidateList.splice(index, 1);
					console.log(candidateList);
					changed = true;
				}

			}
			if(changed){
				$('#show_visualization').click();
			}
		});


	$('#submit_query').click(function(){
		startTime = $("#start").val();
		endTime = $("#end").val();
		interval = $("#interval").val();
		candidate = "Hillary Clinton"

		query = '4#' + startTime + '|' + endTime + '|' + interval + '|' + candidate;

		$.get("/select/" + encodeURIComponent(query), function(data){
			console.log(data)
		});

	})
    //query = '4#1449360000000|1449361000000|10|"Hillary Clinton;"'
    $('#show_visualization').click(function(){
    	initializeTraces();
    	interval = parseInt($('#interval').val());
    	startUNIX = parseInt($('#start').val());

    	endUNIX = parseInt($('#end').val());


		// query = '4#1448081559999|1448082159999|Hillary Clinton;';
		// $.get('/select/' + encodeURIComponent(query), function(data){
		// 	console.log(data);
		// 	var tupleList = deserialize(data["content"]["data"]);
		// 	for(var i = 0; i < tupleList.length; i++){
		// 		console.log(detuple(tupleList[i]));
		// 	}
		// 	// timestamp = 120;
		// 	// value = data["content"]["data"];
		//  //    // old data
		//  //    data = [{x: 1,y: 5},{x: 20,y: 20}, {x: 40,y: 10}, {x: 60,y: 40}, {x: 80,y: 100}, {x: 100,y: 60}]
		//  //    // add new data point to end
		//  //    data.push({x: timestamp, y: value})
		//  //    makeGraph(data);
		//   })

		    for(var i = 0; i < candidateList.length; i++){
		    	var candidate = candidateList[i];


					// var trace = { "x" : [], "y" : [], "type" : "scatter", "line" : { color: 'rgb(55, 128, 191)',}};

					// for(var j = 0; j < timerange.length; j++){

					// 	(function(UNIX_timestamp_ms, candidate, callback){
					// 		query = generateSelectQuery(UNIX_timestamp_ms, candidate);

							// $.get("/select/" + encodeURIComponent(query),
							// 	function(data){
							// 		var trace = {};
							// 		var result = data["content"]["data"];
							// 		trace["candidate"]  = candidate.toString();
							// 		trace["unix_time"] = UNIX_timestamp_ms;
							// 		trace["count"]= result;

							// 		callback(trace);
							// 	});
					// 	})(timerange[j], candidate, addToTraces);

					// }
					(function(startUNIX, endUNIX, candidate, callback){

						query = serialize("4", [startUNIX.toString(), endUNIX.toString(), candidate]);
						$.get("/select/" + encodeURIComponent(query),
							function(data){
								// var result = data["content"]["data"];
								var tupleList = deserialize(data["content"]["data"]);
								var traceList = [];
								for(var j = 0; j < tupleList.length; j++){
									var trace = {};
									var tuple = detuple(tupleList[j]);
									trace["candidate"]  = candidate.toString();
									trace["unix_time"] = tuple[0];
									trace["count"]= tuple[1];
									traceList.push(trace);
								}

								callback(traceList);
						});
					})(startUNIX, endUNIX, candidate, addToTraces);

				}
				console.log("OUT");

			})

function serialize(QueryType_value, data){
			query = QueryType_value; //to Select single datapoint
			query += QTYPE_SEPARATOR;
			query += data.join(DATA_SEPARATOR);
			query += QUERY_SEPARATOR;
			console.log(query);
			return query;
		}

		function timeConverter(UNIX_timestamp){
			var a = new Date(UNIX_timestamp * 1000);
			var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
			var year = a.getFullYear();
			var month = months[a.getMonth()];
			var date = a.getDate();
			var hour = a.getHours();
			var min = a.getMinutes();
			var sec = a.getSeconds();
			var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
			return time;
		}

		function mapX(d){
			// var xList = [];
			// for(var i = 0; i < traceList.length; i++){
			// 	xList = xList.concat(traceList[i].unix_time);
			// }
			// return xList;
			return d.unix_time;
		}

		function mapY(d){
			// var yList = [];
			// for(var i = 0; i < traceList.length; i++){
			// 	yList = yList.concat(traceList[i].count);
			// }
			// return yList;
			return d.count;
		}

		function makeGraph(traceList){

			$('#visualisation').html("");
			var dataGroup = d3.nest()
			.key(function(d) {
				return d.candidate;
			})
			.entries(traceList);

			console.log(dataGroup);

			var vis = d3.select('#visualisation'),
			WIDTH = 1500,
			HEIGHT = 800,
			MARGINS = {
				top: 50,
				right: 50,
				bottom: 50,
				left: 100

			},
			xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(traceList, mapX), d3.max(traceList, mapX)]),
			yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(traceList, mapY), d3.max(traceList, mapY)]),
			xAxis = d3.svg.axis()
			.scale(xRange)
			.tickSize(5)
			.tickSubdivide(true),
			yAxis = d3.svg.axis()
			.scale(yRange)
			.tickSize(5)
			.orient('left')
			.tickSubdivide(true);

			vis.append('svg:g')
			.attr('class', 'x axis')
			.attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
			.call(xAxis);

			vis.append('svg:g')
			.attr('class', 'y axis')
			.attr('transform', 'translate(' + (MARGINS.left) + ',0)')
			.call(yAxis);

			var lineFunc = d3.svg.line()
			.x(function(d) {
				return xRange(d.unix_time);
			})
			.y(function(d) {
				return yRange(d.count);
			})
			.interpolate('linear');

			// for(var i = 0; i < traceList; i++){
			// 	vis.append('svg:path')
			// 	.attr('d', lineFunc(traceList[i]))
			// 	.attr('stroke', 'blue')
			// 	.attr('stroke-width', 2)
			// 	.attr('fill', 'none');
			// }

			dataGroup.forEach(function(d, i) {
				vis.append('svg:path')
				.attr('d', lineFunc(d.values))
				.attr('stroke', function(d, j) {
					return "hsl(" + Math.random() * 360 + ",100%,50%)";
				})
				.attr('stroke-width', 2)
				.attr('fill', 'none');
			});
		}
	})
