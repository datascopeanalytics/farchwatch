var margin = {top:0, right: 0, bottom: 50, left: 40},
    width = 860 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom,
    startDate = new Date(2015,1,1),
    endDate = new Date(2015,6,1),
    // startAge = 20,
    // endAge = 80,
    y = d3.scale.linear().range([height,0]).domain([-30,100]),
    dateme = d3.time.scale().domain([startDate,endDate]).range([1,152]),
    x = d3.time.scale().domain([startDate,endDate]).range([0,width]);
    // years = d3.range(startYear, endYear);

var viz = d3.select("#viz")
    .append("svg:svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

viz.append('rect')
    .attr('class','background')
    .attr('width',width)
    .attr('height',height)


queue()
    .defer(d3.json, "./data_by_year.json")
    .defer(d3.json, "./when_it_be_over.json")
    .await(ready);

function line(feat) { 
    return d3.svg.line()
    .x(function(d) {
	return x(dateme.invert(d.day));
    })
    .y(function(d) {
	tm = parseFloat(d[feat])
	return y(tm);
    });
};

// month axis http://bl.ocks.org/mbostock/1849162
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(d3.time.months)
    .tickSize(16, 0)
    .tickFormat(d3.time.format("%B"));

viz.append('g')
    .attr('class','x axis')
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
.selectAll(".tick text")
    .style("text-anchor", "start")
    .attr("x", 6)
    .attr("y", 6);


var buddy; // so's you can see the data in the console
function ready(error, data, over) {

    data = d3.values(data);
    buddy = data;

    years = viz.selectAll('.year')
	.data(data)
	.enter().append('g')
	.attr('class',function(d){ return 'year '+d[0].year})
    years.append('path')
	.attr('d',line('TMAX'))
	.attr('class','tmax')
    years.append('path')
	.attr('d',line('TMIN'))
	.attr('class','tmin')
	   
    viz.append('line')
	.attr('id','line_of_salvation')
	.attr('x1',x(startDate))
	.attr('x2',x(endDate))
	.attr('y1',y(60))
	.attr('y2',y(60))


    
}