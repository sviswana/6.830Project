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

// initialize axes for graph
makeGraph([])

	timerange = [];
	five_minutes_in_ms = 300000;
	interval = 300000;
	currentTime = 1448082159999; //TODO (change this) : new Date();
	DATA_SEPARATOR = "|";
	QTYPE_SEPARATOR = "#";
	QUERY_SEPARATOR = ";";
	traces = []
  dataList = [];


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

function displayChart(data){
      var w = 400;
  var h = 400;
  var r = h/2;
  var color = d3.scale.category20c();

  var vis = d3.select('#chart').append("svg:svg").data([data]).attr("width", w).attr("height", h).append("svg:g").attr("transform", "translate(" + r + "," + r + ")");
  var pie = d3.layout.pie().value(function(d){return d.value;});

  // declare an arc generator function
  var arc = d3.svg.arc().outerRadius(r);

  // select paths, use arc generator to draw
  var arcs = vis.selectAll("g.slice").data(pie).enter().append("svg:g").attr("class", "slice");
  arcs.append("svg:path")
      .attr("fill", function(d, i){
          return color(i);
      })
      .attr("data-legend",function(d,i) { return data[i].label; })
      .attr("d", function (d) {
          // log the result of the arc generator to show how cool it is :)
          console.log(arc(d));
          return arc(d);
      });

      // add the text
      arcs.append("svg:text").attr("transform", function(d){
        d.innerRadius = 0;
        d.outerRadius = r;
      return "translate(" + arc.centroid(d) + ")";}).attr("text-anchor", "middle").text( function(d, i) {
      return data[i].value;}
      //return data[i].label;}
      );

        legend = vis.append("g")
    .attr("class","legend")
    .attr("transform","translate(50,30)")
    .style("font-size","12px")
    .call(d3.legend)

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


 $('#get_inc_avg').click(function(){
    candidate = $('input[type=radio]:checked').attr('id');

    query = '6#' + candidate + ";";

    $.get("/select/" + encodeURIComponent(query), function(data){
      $("#inc_avg").text(data["content"]["data"]);
      console.log(data["content"]["data"])
    });
    
 })

  $('#show_chart').click(function(){
       candidates = ["Hillary Clinton","Carly Fiorina","Bernie Sanders","Marco Rubio", "Donald Trump", "Ted Cruz", "Ben Carson", "Rand Paul"];
    startTime = $("#start").val();
    endTime = $("#end").val();
    interval = parseInt($('#interval').val()) * five_minutes_in_ms;

    (function(candidates, startTime, endTime, interval,callback){

    for(var i = 0; i < candidates.length; i++){
      var candidate = candidates[i];

      // modify query to do incremental counts later
      query = serialize("4", [startTime, endTime, interval, candidate]);
    $.get("/select/" + encodeURIComponent(query), function(d){
        response = deserialize(d["content"]["data"]);

        tuple = detuple(response[0])
        count = convertToInt(tuple[1])
        current_candidate = tuple[2]

        element = {"label": current_candidate, "value": count}
        callback(element)
    });

    }
    })(candidates, startTime, endTime, interval, addCounts);
 })

  function addCounts(count){
    dataList.push(count);
    if (dataList.length == 8){
      displayChart(dataList);
    }
  }

  $('#get_inc_count').click(function(){
    candidate = $('input[type=radio]:checked').attr('id');
    startTime = $("#start").val();
    endTime = $("#end").val();

    query = '7#' + startTime + '|' + endTime + '|' + candidate + ";";


    $.get("/select/" + encodeURIComponent(query), function(data){
      $("#inc_count").text(data["content"]["data"]);
      console.log(data["content"]["data"])
    });
    
 })

    //query = '4#1449360000000|1449361000000|10|"Hillary Clinton;"'
    $('#show_visualization').click(function(){
    	initializeTraces();
    	interval = parseInt($('#interval').val()) * five_minutes_in_ms;
    	startUNIX = parseInt($('#start').val());

    	endUNIX = parseInt($('#end').val());

		    for(var i = 0; i < candidateList.length; i++){
		    	var candidate = candidateList[i];

					(function(startUNIX, endUNIX, candidate, callback){

						query = serialize("4", [startUNIX.toString(), endUNIX.toString(), interval.toString(), candidate]);
						$.get("/select/" + encodeURIComponent(query),
							function(data){
								// var result = data["content"]["data"];
								var tupleList = deserialize(data["content"]["data"]);
								var traceList = [];
								for(var j = 0; j < tupleList.length; j++){
									var trace = {};
									var tuple = detuple(tupleList[j]);
                  					console.log(tuple[0], convertToInt(tuple[0]))
									trace["candidate"]  = candidate.toString();
									trace["unix_time"] = convertToInt(tuple[0]);
									trace["count"]= convertToInt(tuple[1]);
									console.log(trace["count"]);

									traceList.push(trace);
								}

								callback(traceList);
						});
					})(startUNIX, endUNIX, candidate, addToTraces);

				}
				console.log("OUT");

			})

function convertToInt(timeString){
  return timeString.substring(1, timeString.length-1) * 1;
}

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
			WIDTH = 1000,
			HEIGHT = 600,
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
