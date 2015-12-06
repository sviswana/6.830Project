$(document).ready(function(){

	candidateList = ["Hillary Clinton",
	"Carly Fiorina",
	"Bernie Sanders",
	"Marco Rubio", 
	"Donald Trump", 
	"Ted Cruz", 
	"Ben Carson", 
	"Rand Paul"];
	timerange = [];
	currentTime = 1448082159999; //TODO (change this) : new Date();
	DATA_SEPARATOR = "|";
    QTYPE_SEPARATOR = "#";
    QUERY_SEPARATOR = ";";

	for( var i = 0; i < 5; i++){
		timerange.push(currentTime - (i * 300000));
	}


	$('#show_visualization').click(function(){
		//query = '3#1448082159999|Trump;';
		// $.get('/select/' + encodeURIComponent('3#1448082159999|Trump;'), function(data){
		// 	timestamp = 120;
		// 	value = data["content"]["data"];
		//     // old data
		//     data = [{x: 1,y: 5},{x: 20,y: 20}, {x: 40,y: 10}, {x: 60,y: 40}, {x: 80,y: 100}, {x: 100,y: 60}]
		//     // add new data point to end
		//     data.push({x: timestamp, y: value})
		//     makeGraph(data);
		//   })
			traceList = []
			for(var i = 0; i < candidateList.length; i++){
			   var candidate = candidateList[i];

				
				(function(cand, trList){
					var trace = { "x" : [], "y" : [], "type" : "scatter", "line" : { color: 'rgb(55, 128, 191)',}};

					for(var j = 0; j < timerange.length; j++){

						(function(UNIX_timestamp_ms, candidate, trace){
							query = generateSelectQuery(UNIX_timestamp_ms, candidate);
							$.get("/select/" + encodeURIComponent(query),
								function(data){
									var result = data["content"]["data"];
									trace["x"].push(UNIX_timestamp_ms);
									trace["y"].push(result);
									console.log(candidate.toString());
									//console.log(trace);
							});
						})(timerange[j], cand, trace);

					}
					trList.push(trace);
				})(candidate, traceList);

				console.log(traceList);
				
			}
		})

		function generateSelectQuery(UNIX_timestamp_ms, candidate){
			query = "3"; //to Select single datapoint
			query += "#";
			query += UNIX_timestamp_ms.toString();
			query += "|";
			query += candidate;
			query += ";"
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

		function makeGraph(lineData){
			var vis = d3.select('#visualisation'),
			WIDTH = 1000,
			HEIGHT = 500,
			MARGINS = {
				top: 20,
				right: 20,
				bottom: 20,
				left: 50
			},
			xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(lineData, function(d) {
				return d.x;
			}), d3.max(lineData, function(d) {
				return d.x;
			})]),
			yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(lineData, function(d) {
				return d.y;
			}), d3.max(lineData, function(d) {
				return d.y;
			})]),
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
				return xRange(d.x);
			})
			.y(function(d) {
				return yRange(d.y);
			})
			.interpolate('linear');

			vis.append('svg:path')
			.attr('d', lineFunc(lineData))
			.attr('stroke', 'blue')
			.attr('stroke-width', 2)
			.attr('fill', 'none');
		}
	})
