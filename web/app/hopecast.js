
// var today = d3.time.day.floor(new Date())
// var enddate = d3.time.day.offset(today,10)
// var tenday = d3.time.day.range(today,enddate)
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

queue()
    .defer(d3.json, "./forecast.json")
    .await(dopecast);


function dopecast(error, tenday){

    console.log(tenday)

    var hopecast = d3.select('#hopecast-container').append('svg')
	.attr('width',hopewidth)
	.attr('height',hopeheight)
	.attr('id','hopecast')
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
	.style('stroke-dasharray','2 2')
	.style('fill','none')

    
    var day_header = hopecast.append('g')
	.attr('transform','translate('+padding/2+','+padding/2+')')
	.attr('class','day-header')
    
    day_header.append('rect')
	.attr('height',dayheight/5-padding)
	.attr('width',daywidth-padding)
    
    day_header.append('text')
	.attr('x',(daywidth-padding)/2)
	.attr('y',daywidth/10)
	.attr('dy','0.5em')
	.attr('text-anchor','middle')
	.text(function(d){
	    return d.weekday+' '+d.date;
	})

    var farchlook = hopecast.append('g')
	.attr('transform','translate('+padding/2+','+(dayheight*3/4)+')')
	.attr('class','farchlook')

    farchlook.append('rect')
	.attr('width',daywidth-padding)
	.attr('height',dayheight/4-padding/2)

    farchlook.append('text')
	.attr('x',(daywidth-padding)/2)
	.attr('y',dayheight/8)
	.attr('dy','0.2em')
	.attr('text-anchor','middle')
	.text(function(d){
	    return d.outlook;
	})

    var conditions = hopecast.append('g')
	.attr('transform','translate('+ 2*padding +','+ (dayheight/5 + padding)+')')
	.attr('class','conditions')

    conditions.append('rect')
	.attr('width',daywidth-4*padding)
	.attr('height',dayheight*2/5-2*padding)
	.style('stroke','darkgray')
	.style('stroke-width','1px')
	.style('stroke-dasharray','2 2')
	.style('fill','none')

    conditions.append('image')
	.attr('width',daywidth-4*padding)
	.attr('height',dayheight*2/5-2*padding)
	.attr('xlink:href','cool_icon.png') 
	.attr('class',function (d){
	    return 'conditions-icon '+ 'con_'+d.icon
	})


    var hilo = hopecast.append('g')
	.attr('transform','translate(' + 2*padding + ',' + (dayheight*3/5) + ')')
	.attr('class','hilo')

    hilo.append('text')
	.attr('x',(daywidth-4*padding)/2)
	.attr('y',dayheight/10)
	.attr('text-anchor','middle')
	.text(function(d){
	    return d.high + ' / ' + d.low;
	})
	.style('fill','black')

    
}
