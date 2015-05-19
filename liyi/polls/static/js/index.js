var width,svg, project,path,height = 800;
var data,proYear,time = 2004,province="",ngoList = [],nowTimeId = -1,nodeChosen;
var color = d3.scale.category20();

d3.json("/static/data/provinceYearNum.json",function(error,root){
	if(error)
		return console.error(error);
	proYear = root;
});
d3.json("/static/data/china.json", function(error, root) {
	if (error)
		return console.error(error);
	data = root;
	// console.log(root.features);
	update();
	drawInfo();
	drawTimeAxis();
});

function update(){
	updateMap();
	updateNgoList(1);
}
var perPageNumber = 15;
function updateNgoList(page){

	div = d3.select("#ngoList").select("#listGroup");
	if(div) div.remove();
	h3 = d3.select("#ngoList").select("h3")
	if(h3) h3.remove();
	h3 = d3.select("#ngoList").append("h3").text("NGO列表:");
	div = d3.select("#ngoList").append("div").attr("id","listGroup");
	var number = ngoList.length;
	var pages = Math.ceil(number/perPageNumber);
	var ngoListToShow;
	var start = (page-1)*perPageNumber,end = Math.min(start + perPageNumber,number);
	ngoListToShow = ngoList.slice(start,end);
	// console.log(ngoListToShow);
	dataPage = new Array();
	for(var i = 1;i <= pages; i++)dataPage.push(i);
	div.attr("class","list-group");
	a = div.selectAll("a").data(ngoListToShow).enter()
		   .append("a")
		   .attr("class","list-group-item")
		   .text(function(d,i){
		   	return  d.name;  
		   })
		   .on("mouseover",mouseOver)
		   .on("mouseout",mouseOut)
		   .on("click",clickItem);
	function mouseOver(d,i){
		d3.select(this).classed("active",true);
	}
	function mouseOut(){
		d3.select(this).classed("active",false);
	}
	function clickItem(d,i){
		var dataSend = JSON.stringify({"nodeID":d.id})
		$.ajax({
			type:"post",
			data:dataSend,
			url:"/searchSingle/",
	        processData: false,
	        contentType:"application/json; charset=utf-8",
	        dataType: "json",
	        success: function(node) { // data is json,include ngo in the given province and time
	        	nodeChosen = node;
	        	var svgId = "#mainKnowledgeBase";
	        	render(nodeChosen,svgId);
	      	}
		});
	}
	//pagination
	pagination = d3.select("#ngoList").select("#pageFoot");
	if(pagination)pagination.remove();
	pagination = d3.select("#ngoList").append("div").attr("id","pageFoot");
	ul = pagination.append("ul").attr("class","pagination");
	ul.selectAll("li").data(dataPage).enter()
	  .append("li")
	  .attr("id",function(d){return "page"+d;})
	  .append("a")
	  .text(function(d){return d;})
	  .on("click",liClick);
	ul.select("#page"+page).classed("active",true);
	function liClick(d,i){
		console.log(d);
		ul.select(".ative").classed("active",false);
		d3.select(this.parentNode).classed("active",true);
		updateNgoList(d);
	}
}
function updateMap(){
	var tooltip = d3.select("#tooltip");
	svg = d3.select("#china").select("svg");
	if(svg) svg.remove();
	svg = d3.select("#china").append("svg")
		.attr("width", "100%")
		.attr("height", height)
		.attr("id","chinaMapSvg")
		.append("g")
		.attr("transform", "translate(0,0)");
	var width = $("#chinaMapSvg").innerWidth();
	// console.log("width:",width,"  height: ",height);
	var projection = d3.geo.mercator()
		.center([107, 31])
		.scale(850)
		.translate([width / 2, height*2 / 3]);

	var path = d3.geo.path()
		.projection(projection);

	svg.selectAll("path")
		.data(data.features)
		.enter()
		.append("path")
		.attr("stroke", "#000")
		.attr("stroke-width", 1)
		.attr("fill", function(d, i) {
			return color(i);
		})
		.attr("d", path)
		.on("mouseover", mouseOver)
		.on("mouseout",mouseOut)
		.on("dblclick",dblclick);
	function mouseOver(d,i){
			s = d3.select(this);
			var name = d.properties.name;
			// console.log(name);
			s.attr("fill", "yellow");
			var left = d3.event.pageX,top = d3.event.pageY;
			// console.log(d3.event.pageX,d3.event.pageY);
			tooltip.style("left",left+"px")
				   .style("top",top+"px")
			tooltip.select("#province").text(d.properties.name);
			tooltip.select("#value").text(function(){
				console.log(proYear);
				for(var i =0; i < proYear.length; i++){
					if(proYear[i]['year'] == time){
						return proYear[i][time.toString()][name].total;
					}
				} 
			});
			tooltip.select("#time").text(function(){
				if(time == 2004) return "不限";
				if(time == 2005) return "<2006"
				return time;
			});
			tooltip.classed("hidden",false);
	}
	function mouseOut(d,i){
		s = d3.select(this);
		s.attr("fill",color(i));
		tooltip.classed("hidden",true);
	}
	function dblclick(d,i){
		province = d.properties.name;
		d3.select("#provinceChosen").text(sPro+province);
		var dataSend = JSON.stringify( {"province":province,"time":time}) ;
		$.ajax({
			type:"post",
			data:dataSend,
			url:"/searchProvinceTime/",
	        processData: false,
	        contentType:"application/json; charset=utf-8",
	        dataType: "json",
	        success: function(newData) { // data is json,include ngo in the given province and time
	        	ngoList = newData['ngoList'];
	        	updateNgoList(1);
	      	}
		});
	}
}
var sPro = '选中的省份: ',sYear = '选中的时间: ';
function drawInfo(){
	var mapSvg = d3.select("#china").select("svg");
	if(mapSvg){
		var infoBox = mapSvg.select("#infoBox");
		if(infoBox)infoBox.remove();
		rect = mapSvg.append("rect").attr("id","infoBox")
						.attr("x",10)
						.attr("y",10)
						.attr("width",200)
						.attr("height",50)
		mapSvg.append("text").attr("id","provinceChosen")
							.attr("x",20)
							.attr("y",30)
							.html(function(){
								return sPro+'不限';
							});
		mapSvg.append("text").attr("id","yearChosen")
							  .attr("x",20)
							  .attr("y",50)
							  .html(function(){
									return sYear+'不限';
								});
		}
}

function drawTimeAxis(){
	var h3 = d3.select("#timeRow").select("h3");
	if(h3) h3.remove();
	d3.select("#timeRow").append("h3").append("b").text("成立时间：");
	timeScale = new Array();
	for(i = 2004; i < 2016;i++)
		timeScale.push(i);
	timeAxis = d3.select("#timeRow").select("svg");
	if(timeAxis)timeAxis.remove;
	timeSvg = d3.select("#timeRow").append("svg")
				.attr("width","1030px")
				.attr("height","80px")
				.attr("id","timeSvg");
	var x1 = 20,y1 = 20;
	var x2 = 1030,y2 = y1;
	timeLine = timeSvg.append("line").attr("id","timeLine")
			   .attr("x1",x1)
			   .attr("y1",y1)
			   .attr("x2",x2)
			   .attr("y2",y2)
			   .attr("stroke","green")
			   .attr("stroke-width",5);
	var r=8,newr = 12,color = "red",newColor = "yellow";
	circles = timeSvg.selectAll("circle").data(timeScale).enter()
			  .append("circle")
			  .attr("id",function(d){return "circle"+d})
			  .attr("cx",function(d,i){
			  	return 87*i+30;
			  })
			  .attr("cy",y1)
			  .attr("r",r)
			  .attr("fill",color)
			  .on("click",click)
			  .on("mouseover",mouseOver)
			  .on("mouseout",mouseOut);
	timeText = timeSvg.selectAll("text").data(timeScale).enter()
				.append('text')
				.attr("x",function(d){
					circle = d3.select("#circle"+d);
					// console.log(circle.attr("cy"));
					return circle.attr("cx") - 15;
				})
				.attr("y",function(d){
					// return 30; 
					circle = d3.select("#circle"+d);
					return parseInt(circle.attr("cy"))+parseInt(circle.attr("r")) + parseInt(15);
				})
				.text(function(d){
					if(d == 2004){
						return "不限";
					}
					else if(d == 2005){
						return "<2006";
					}
					else return d;
				});
	function mouseOver(d,i){
		d3.select(this).attr("r",newr);
	}
	function mouseOut(d,i){
		d3.select(this).attr("r",r);
	}
	function click(d,i){
		d3.select("#circle"+time).attr("fill",color);
		time = d;
		var tem;
		if(time == 2004)tem = "不限";
		else if(time == 2005) tem = "<2006";
		else tem = time;
		d3.select("#yearChosen").text(sYear+tem)
		d3.select(this).attr("fill","yellow");
	}

}