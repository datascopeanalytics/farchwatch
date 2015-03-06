Firebase.goOffline();

var margin = {top:10, right: 0, bottom: 50, left:40},
    width = $("#viz").width() - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom,
    startDate = new Date(2015,0,1),
    endDate = new Date(2015,5,1),
    y = d3.scale.linear().range([height,0]).domain([-30,100]),
    x = d3.time.scale().domain([startDate,endDate]).range([0,width]),
    dateme = d3.time.scale().domain([startDate,endDate]).range([1,151]);

var nice_thresh, not_over_thresh;
var tolerance = 1;

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
    .defer(d3.json, "./daily_averages.json")
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
function area() {
    return d3.svg.area()
        .x(function(d) {
            return x(dateme.invert(d.day));
        })
        .y0(function(d) {
            tm = parseFloat(d["TMAX"])
            return y(tm);
        })
        .y1(function(d) {
            tm = parseFloat(d["TMIN"])
            return y(tm);
        });
}

// month axis http://bl.ocks.org/mbostock/1849162
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(d3.time.months)
    .tickSize(16, 0)
    .tickFormat(d3.time.format("%B"));

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(8)
    .outerTickSize(0)

viz.append('g')
    .attr('class','x axis')
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
.selectAll(".tick text")
    .style("text-anchor", "start")
    .attr("x", 6)
    .attr("y", 6);

viz.append('g')
    .attr('class','y axis')
    .call(yAxis);

var all_colors = ["color1","color2","color3","color4","color5"].reverse();
var available_colors = all_colors.slice(0);
var key_div = d3.select('#yearlist');
var num_selected = 0;

//console goodness part 1
var whenit;
var buddy; 
var dailies;

function ready(error, data, over, averages) {

    data_array = d3.values(data);

    // console goodness part 2
    buddy = data;
    whenit = over;
    dailies = averages;

    var year_list = d3.keys(data).map(function(d){return +d}).reverse()

    years = viz.selectAll('.year')
        .data(data_array)
        .enter().append('g')
        .attr('class',function(d){return 'year year-'+d[0].year});
    years.append('path')
        .attr('d',area())
        .attr('class','temparea');

    viz.append('line')
        .attr('id','line_of_salvation')
        .attr('x1',x(startDate))
        .attr('x2',x(endDate))
        .attr('y1',y(60))
        .attr('y2',y(60));

    // add years to scrollbox;
    key_div.selectAll(".yearbox")
        .data(year_list)
        .enter().append('div')
        .attr('class','key-year')
    .attr('data-year',function(d){return d;})
        .html(function(d){return d;})
    .on('mouseenter',hoveryear)
    .on('mouseleave',unhoveryear)
        .on("click", function(year, index) {
            if($(this).hasClass('selected-box')) {
                num_selected -= 1;
            }
            else {
                num_selected += 1;
            }
            if(num_selected <= 5) {
                var lineclass = ".year-" + year;

                console.log(d3.select(this));

                if($(this).hasClass('selected-box')) {
                    console.log('remove color');
                    recycleColor(this, lineclass);
                }
                else {
                    console.log('add color');
                    addUniqueColor(this, lineclass);
                }

                $(this).toggleClass('selected-box');
                // toggles the class depending on whether it's selected or not

                var yearline = d3.select(lineclass);
                yearline.classed('selected-line',
                                 !yearline.classed('selected-line'));
            }
            else {
                num_selected -= 1;
                alert('Cut it out, Captain Clickhappy. '+
                      'You can only select 5 years at a time.');
            }
            console.log('selected', num_selected);

        })

    makeGradient();

    $('#comment-submit').on('click', postComment);
    function whenover(year){

    fuck = new Date(over[year][tolerance]);
    dateover = new Date(2015,fuck.getMonth(),fuck.getDay())
    return dateover;
    }

    function hoveryear() {
    year = $(this).data('year');
    var hoverline = viz.selectAll('.hovered-line')
        .data([data[year]])
        .enter().append('g')
        .attr('class','hover hovered-line')
    hoverline.append('path')
        .attr('d',line('TMAX'))
        .attr('class','tmax')
    hoverline.append('path')
        .attr('d',line('TMIN'))
        .attr('class','tmin')
    dateover = whenover(year);
    // console.log(year)
    // console.log(dateover)
    viz.append('rect')
        .attr('x',x(dateover))
        .attr('y',0)
        .attr('width',width-x(dateover))
        .attr('height',height)
        .attr('class','hover hovered-over')

    };

    function unhoveryear() {
    year = $(this).data('year');
    viz.selectAll('.hover')
        .data([])
        .exit().remove()
    };


}

function addUniqueColor(box, line) {
    var color = available_colors.pop();
    d3.select(box).classed(color, true);
    d3.select(line).classed(color, true);
}
function recycleColor(box, line) {
    for(var i=0; i<all_colors.length; i++) {
        if(d3.select(box).classed(all_colors[i])){
            d3.select(box).classed(all_colors[i], false);
            d3.select(line).classed(all_colors[i], false);
            available_colors.push(all_colors[i]);
        }
    }
}

function makeGradient() {
     viz.append("linearGradient")
      .attr("id", "temperature-gradient")
      .attr("gradientUnits", "userSpaceOnUse")
      .attr("x1", 0).attr("y1", y(-30))
      .attr("x2", 0).attr("y2", y(100))
    .selectAll("stop")
      .data([
          {offset: "0%", color: "black"},
          {offset: "30%", color: "#6060ff"},
          {offset: "60%", color: "#dddddd"},
          {offset: "70%", color: "#ffff20"},
          {offset: "100%", color: "red"}
      ])
    .enter().append("stop")
      .attr("offset", function(d) { return d.offset; })
      .attr("stop-color", function(d) { return d.color; });

}

function postComment() {
    Firebase.goOnline();
    var commentBox = $("#comment");
    var fb = new Firebase("https://boiling-fire-9934.firebaseio.com/");
    comments = fb.child("comments");
    comments.push({"message":commentBox.val()})

    commentBox.val("");
    alert("Cool. We'll maybe read that at some point.")
}

function niceDaysPerMonth(){
    //mean nice days inverse month
    var my = d3.nest()
	.key(function (d) {return d.month+'_'+d.year})
	//.key(function (d) {return d.year})
	.rollup(function (d) {
	    c = d3.sum(d,function(g){
		return g.is_nice;
	    });
	    x = d3.max(d, function(g){
		return g.TMAX;
	    });
	    n = d3.min(d, function(g){
		return g.TMIN;
	    });
	    mx = d3.mean(d,function(g){
		return g.TMAX;
	    });
	    mn = d3.mean(d,function(g){
		return g.TMIN;
	    });

	    return {
		month:d[0].month,
		year:d[0].year,
		nice_day_count: c,
		highest_high: x,
		lowest_low: n,
		average_high: trunc(mx,1),
		average_low: trunc(mn,1)
	    }
	})
	.entries(d3.merge(d3.values(buddy)))


    var mo = d3.nest()
	.key(function(d){return d.values.month})
	.rollup(function (d) {
    	    goods = d3.sum(d,function(g){
    		return g.values.nice_day_count;
    	    })
    	    exten = d3.extent(d,function(g){
    		return g.values.nice_day_count;
    	    });
	    hhh = d3.max(d,function(g){
		return g.values.highest_high;
	    });
	    exah = d3.extent(d,function(g){
		return g.values.average_high;
	    });
	    lll = d3.min(d,function(g){
		return g.values.lowest_low;
	    });
	    exal = d3.extent(d,function(g){
		return g.values.average_low;
	    });
	    var raw = []
	    for (y in d) {
	    	raw.push(d[y].values);
	    }
    	    return {
    		total_nice_days: goods,
    		mean_nice_days: trunc(goods/d.length,1),
    		min_nice_days: exten[0],
    		max_nice_days: exten[1],
		highest_highest_high: hhh,
		lowest_average_high: exah[0],
		highest_average_high: exah[1],
		lowest_average_low: exal[0],
		highest_average_low: exal[1],
		lowest_lowest_low: lll,
		raw:raw
	    }
    	})
    
    	.entries(my)

    var mz = d3.nest().key(function(d){return d.values.year})
	.rollup(function(d) {
	    return d.map(function(g){
		return g.values;
	    }) 
	})
	.entries(my)


    mz.forEach(function(d){
	console.log('d',d);
	ytnd = d3.sum(d,function(g){
	    console.log('g',g);
	    ndc = g.values.nice_day_count;
	    console.log('ndc',ndc);
	    return ndc;
	});
	console.log('ytnd',ytnd)
	d['year_total_nice_days'] = ytnd
    })

//	.entries(d3.merge(d3.values(buddy)))
//	.entries(d3.merge(d3.values(buddy)))
    return [my,mo,mz];
}



function trunc(num,places){
    p = Math.pow(10,places)
    return Math.round(num*p)/p
}
