
var today = new Date()
var tenday = d3.time.day.range(today,d3.time.day.offset(today,10))
console.log(tenday)
var padding = 5
var hopewidth = $('#hopecast-container').width()
//var hopeheight = $('#hopecast-container').height()
var hopeheight = 150;
var daywidth = (hopewidth-padding)/10 - padding;
var dayheight = hopeheight-(padding * 2)

function scooch(i){
    return padding + i*(daywidth+padding)
}

var daynames = {
    0:'Sun',
    1:'Mon',
    2:'Tue',
    3:'Wed',
    4:'Thu',
    5:'Fri',
    6:'Sat',
    7:'Sun'
}

var hopecast = d3.select('#hopecast-container').append('svg')
    .attr('width',hopewidth)
    .attr('height',hopeheight)
    .attr('class','hopecast-svg')
    .selectAll('.day')
    .data(tenday)
    .enter().append('g')
    .attr('class','day')
    .attr('transform',function(d,i){
	return 'translate('+scooch(i)+',0)'
    })

hopecast.append('rect')
    .attr('height',dayheight)
    .attr('width',daywidth)
    .style('stroke','darkgray')
    .style('fill','none')

hopecast.append('rect')
    .attr('x',padding/2)
    .attr('y',padding/2)
    .attr('height',dayheight/5-padding)
    .attr('width',daywidth-padding)

hopecast.append('text')
    .attr('x',daywidth/2)
    .attr('y',dayheight/10)
    .attr('dy','0.4em')
    .attr('text-anchor','middle')
    .text(function(d){
	return daynames[d.getDay()]+' '+d.getDate();
    })
    .style('fill','white')

