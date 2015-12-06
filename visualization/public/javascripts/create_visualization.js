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
	traces = []

	for( var i = 0; i < 5; i++){
		timerange.push(currentTime - (i * 300000));
	}

	function initializeTraces(){
		traces = [];
	}

	function addToTraces(trace){
		traces.push(trace);
		if(traces.length >= (candidateList.length * timerange.length)){
			traces.sort(function(a,b) {return (a.unix_time > b.unix_time) ? 1 : ((b.unix_time > a.unix_time) ? -1 : 0);} );
			console.log(traces);
			makeGraph(traces);
		}

	}

	$('input[type=checkbox]').change(
	    function(){
	    	console.log("checkbox")
	    	var id = $(this).attr('id');
	    	var index = candidateList.indexOf(id);

	        if (this.checked) {
	        	if(index <= -1){
	        		candidateList.push(id);
	        	}

	        }
	        else{
	        	if(index > -1){
	        		candidateList.splice(index, 1);
	        	}

	        }
	        $('#show_visualization').click();
    });

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
	for(var i = 0; i < candidateList.length; i++){
		var candidate = candidateList[i];


					// var trace = { "x" : [], "y" : [], "type" : "scatter", "line" : { color: 'rgb(55, 128, 191)',}};

					for(var j = 0; j < timerange.length; j++){

						(function(UNIX_timestamp_ms, candidate, callback){
							query = generateSelectQuery(UNIX_timestamp_ms, candidate);
							$.get("/select/" + encodeURIComponent(query),
								function(data){
									var trace = {};
									var result = data["content"]["data"];
									trace["candidate"]  = candidate.toString();
									trace["unix_time"] = UNIX_timestamp_ms;
									trace["count"]= result;

									// console.log(candidate.toString());
									// console.log(trace);

									callback(trace);
								});
						})(timerange[j], candidate, addToTraces);

					}

					// console.log("TL");
					// console.log(traces);



				}
				console.log("OUT");

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
			var dataGroup = d3.nest()
			.key(function(d) {
				return d.candidate;
			})
			.entries(traceList);

			console.log(dataGroup);

			var vis = d3.select('#visualisation'),
			WIDTH = 2000,
			HEIGHT = 500, //$('#visualisation').attr('height'),
			MARGINS = {
				top: 50,
				right: 50,
				bottom: 50,
				left: 200
			},
			xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(traceList, mapX), d3.max(traceList, mapX)]),
			yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(traceList, mapY), d3.max(traceList, mapY)]),
			xAxis = d3.svg.axis()
			.scale(xScale),
			// .tickSize(5)
			// .tickSubdivide(true),
			yAxis = d3.svg.axis()
			.scale(yScale)
			// .tickSize(5)
			.orient('left');
			// .tickSubdivide(true);

			lSpace = WIDTH/dataGroup.length;


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
				return xScale(d.unix_time);
			})
			.y(function(d) {
				return yScale(d.count);
			})
			.interpolate('linear');



			// for(var i = 0; i < traceList; i++){
			// 	vis.append('svg:path')
			// 	.attr('d', lineFunc(traceList[i]))
			// 	.attr('stroke', 'blue')
			// 	.attr('stroke-width', 2)
			// 	.attr('fill', 'none');
			// }

			dataGroup.forEach(function(d, i) 
			{	
				console.log("D");
				console.log(d)
				vis.append('svg:path')
				.attr('d', lineFunc(d.values))
				.attr('stroke', function(d, j) {
					return "hsl(" + Math.random() * 360 + ",100%,50%)";
				})
				.attr('stroke-width', 2)
				.attr('fill', 'none');

				vis.append("text")
			    .attr("x", (lSpace / 2) + i * lSpace)
			    .attr("y", HEIGHT)
			    .style("fill", "black")
			    .text(d.key);
			});

			console.log(vis);
		}
	})
