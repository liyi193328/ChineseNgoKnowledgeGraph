function appendMultiText(container, str){
      
      //获取分割后的字符串
      l = str.length;
      var strs;
      if(l > 6){
        strs = [str.substring(0,l/2),str.substring(l/2,l)];
      }
      else{
        strs = [str];
      }
      var mulText = container.selectAll("text");
      
      tspanSelect = mulText.selectAll("tspan")
      if(tspanSelect){
        // console.log("find have!");
        tspanSelect.remove();
      }
      mulText.append("tspan")
             .attr("dx","0em")
             .attr("dy","0em")
             .text(strs[0]);
      if(l > 6){
        mulText.append("tspan")
               .attr("dx",-l/2-(0.5)+"em")
               .attr("dy","1.5em")
               .text(strs[1]);
      }
      return mulText;
}

function preData(dataSet){
  nodes = dataSet.nodes;
  for(var i=0; i < nodes.length; i++){
    if(nodes[i]['connectionInfo'] != null){
      nodes[i]['connectionInfo'] = nodes[i]['connectionInfo'].replace(/\n/g,"<br />");
    }
    if(nodes[i]['description'] != null){
      nodes[i]['description'] = nodes[i]['description'].replace(/\n/g,"<br />");
    }
  }
  dataSet.nodes = nodes;
  for(var i = 0;i < nodes.length; i++){
    st = nodes[i].nodesID.toString();
    if(clickListFlag[st] != true){
      clickListFlag[st] = false;
    }
  }
  return dataSet;
}
var clickListFlag = new Array();
function render(dataSet,svgId){
    // console.log(dataSet.nodes);
    var dict = new Array();
    dict["time"] = "EsTime",
    dict["ngo"] = "name",
    dict["province"] = "Province",
    dict["sponsors"] = "name",
    dict["field"] = "Field",
    dict["connectionInfo"] = "name",
    dict["orgType"] = "OrgType",
    dict["partners"] = "name";

    colors10 = d3.scale.category10().domain(d3.range(0,10));
    colors20 = d3.scale.category20().domain(d3.range(0,20));
    function colorCal(number){
      return (number*2+1);
    }
    //the color map of laybes
    var colorMap = new Array();
    linkTypes = ['省份','领域','成立时间','联系信息','机构类型','资助','合作伙伴'];
    laybels = ['field','partners','orgType','time','ngo','connectionInfo','sponsors','province'];
    colorMap['field'] = 0,colorMap['partners'] = 1, colorMap['orgType'] = 4,colorMap['time'] = 3,
    colorMap['ngo'] = 2, colorMap['connectionInfo'] = 5,colorMap['sponsors'] = 6, colorMap['province'] = 7;
    //color of links type
    colorMap['省份'] = 15,colorMap['领域'] = 1,colorMap['成立时间'] = 7,colorMap['联系信息']=11,colorMap['机构类型']=9,
    colorMap['资助']=13,colorMap['合作伙伴']=16;

    var width = $(svgId).width(),
        height = 600;
    width = 1200;
    var svg = d3.select(svgId)
                .attr({
                  "width":"100%",
                  "height":height
                });

    var marker = svg.selectAll("defs").data(linkTypes).enter()
            .append('defs')
            .append('marker')
            .attr("id", function(d,i){
              return d;
            })
            .attr("refX", 12.1)
            .attr("refY", 0)
            .attr("markerWidth", 5)
            .attr("markerHeight", 5)
            .attr("viewbox","-5 -5 10 10")
            .attr("orient", 'auto')
            .attr("overflow","visible")
            .append('path')
            .attr("d", 'M 0,0 m -2,-2 L 2,0 L -2,2 Z')
            .style("fill",function(d){
              return colors20(colorMap[d]);
            })

    var force = d3.layout.force()
                  .linkDistance(150)
                  .charge(-1000)
                  .gravity(.05)
                  .size([width, height])
                  .on("tick", tick);

    var link,node,nodes,links,nodesID,nodesLabels,nodesNgo;
    var linkText;
    var r = 30,newR = 40;
      /* Initialize tooltip */
    var tip = d3.tip().attr('class', 'd3-tip').html(function(d) { 
      var type = d.nodesLabels;
      var nameMap = new Array();
      nameMap['name'] = '名字',nameMap['location'] = '地址', nameMap['connectionInfo'] = '联系信息';
      // console.log(type);
      var s = ""
      if(type == "field" || type == 'orgType' || type == 'time' || type == 'province'){
        s = "标签："+ type;
      }
      if(type == 'sponsors' || type == 'partners'){
        s = type;
      }
      if(type == 'ngo'){
        s = '<dl class="dl-horizontal">'
        var property = ['name','location'];
        for(var i = 0; i<property.length; i++){
          s += '<dt>'+nameMap[ property[i] ]+'</dt>';
          var temPro = d[ property[i] ];
          s += '<dd>'+ temPro +'</dd>';
        }
        s += '<dt>'+"标签"+"</dt>";
        s += '<dd>' + type + '</dd>';
        s += '</dl>';
      }
      if(type == 'connectionInfo'){
        s = '<dl class="dl-horizontal">';
        var property = ['name','connectionInfo'];
        for(var i = 0; i<property.length; i++){
          s += '<dt>'+nameMap[ property[i] ]+'</dt>';
          var temPro = d[ property[i] ];
          s += '<dd>'+temPro+'</dd>';
        }
        s += '<dt>'+"标签"+"</dt>";
        s += '<dd>' + type + '</dd>';
        s += '</dl>';
      }
      // console.log(s);
      return s;
    });
    /* Invoke the tip in the context of your visualization */
    var vis = svg.call(tip);

    nodes = dataSet.nodes;
    var searchResult = "";
    if(Number( dataSet.flag) == 0){
      searchResult += "搜索出"+ dataSet.count + "个NGO;";
    }
    else{
      searchResult = ""
      // searchResult += dataSet.count +"条路径;";
    }
    d3.select("#searchNgoNumber").text(searchResult);
    // if(nodes != null){
    //   nodes[0].x = width/2;
    //   nodes[0].y = height/2;
    // }
    // nodes[0]['x'] = width/2;
    // nodes[0]['y'] = height/2;
    function updateNgoNodes(){
      nodesNgo = new Array();
      for(var i = 0; i < nodes.length; i++){
        if( nodes[i].nodesLabels == 'ngo' ){
          nodesNgo.push(nodes[i]);
        }
    }
   }
  function drawKnowGraph(dataSet){ //drawKnowGraphe nodes and links
        dataSet = preData(dataSet);
        width = $(svgId).width();
        // console.log(width);
        svg = d3.select(svgId)
                    .attr({
                      "width":"100%",
                      "height":height
                    });
        nodes = dataSet.nodes;
        links = dataSet.links;
        nodesID = nodes.nodesID;

        lines = svg.selectAll(".link");
        lines.remove();
        circles = svg.selectAll(".node");
        circles.remove();
        svg.selectAll(".linkText").remove();
        link = svg.selectAll(".link"),
        node = svg.selectAll(".node");
        // start the force layout.
        force
            .nodes(nodes)
            .links(links);

        updateNgoNodes();
        d3.select("#ngoNumber").text("目前图谱中有"+nodesNgo.length + "个NGO");

        var drag = force.drag()
                  .on("dragstart",function(d,i){
                      tip.hide(nodes[i].nodesLabels);
                      // console.log("start drag");
                      d3.select(this).classed("fixed", d.fixed = true);//when the node is dragged, we fix the node,click aciton unfix
                     })
                  .on("drag",function(d,i){
                    // console.log("dragging!");
                    tip.hide(nodes[i].nodesLabels);
                    d3.select(this).classed("fixed", d.fixed = true);
                    })
                  .on("dragend",function(d,i){
                    // console.log("endDrag!")
                    })

        // update links.
        link = link.data(links);
        link.enter().append("line")
            .attr("class", "link")
            .attr("id",function(d,i){
              return "link"+i;
            })
            .style("stroke",function(d,i){
              var type = d.type;
              // console.log(20,type,colorMap[type],colors20(colorMap[type]));
              return colors20(colorMap[type]);
            })
            .style("marker-end",function(d){
              var type = d.type;
              // console.log(type);
              var st = "url(#"+type+")";
              return st;
            });

        linkText = svg.selectAll(".linkText").data(links)
                      .enter()
                      .append("text")
                      .attr("dx",-8)
                      .attr("class","linkText")
                      .text(function(d){
                        return d.type;
                      });
        // update nodes.
        node = node.data(nodes);
        var nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("id",function(d,i){return "node"+i;})
            .on("click",click)
            .on("dblclick", dbclick)  // the action fo single click
            .on("mouseover",mouseOver)//the action of mouse stay
            .on("mouseout",mouseOut)  // the action of mouse leave
            .call(drag);

        nodeEnter.append("circle")
                 .attr("r", function(d,i){
                  var st = d.nodesID.toString();
                    if(clickListFlag[st] == true){
                      return newR;
                    }
                    else return r;
                  })
                 .style("fill",function(d,i){
                    var st = d.nodesID.toString();
                    if(clickListFlag[st] == true){
                      return "yellow";
                    }
                    var label = d.nodesLabels;
                    // console.log(10,label,colorMap[label],colors10(colorMap[label]));
                    return colors10(colorMap[label]);
                  });

        nodeEnter.append("text");

        for(var i=0;i<nodes.length;i++){
            container = svg.select("#node"+i);
            showPro = dict[nodes[i].nodesLabels];
            var str = nodes[i][showPro];
            appendMultiText(container,str);
          }
        //start force
        force.start();
  }

  var perPageNumber = 15;
  function updateNgoList(page){
    div = d3.select("#nowNgoList").select("#listGroup");
    if(div) div.remove();
    h3 = d3.select("#nowNgoList").select("h3")
    if(h3) h3.remove();
    h3 = d3.select("#nowNgoList").append("h3").text("NGO列表:");
    div = d3.select("#nowNgoList").append("div").attr("id","listGroup");
    var number = nodesNgo.length;
    var pages = Math.ceil(number/perPageNumber);
    var ngoListToShow;
    var start = (page-1)*perPageNumber,end = Math.min(start + perPageNumber,number);
    ngoListToShow = nodesNgo.slice(start,end);
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
      console.log(d.nodesID);
      for(var i = 0; i < nodes.length ; i++){
        if(nodes[i].nodesID == d.nodesID){
          st = (d.nodesID).toString();
          clickListFlag[st] = true;
          drawKnowGraph(dataSet);
          break;
        }
      }
    }
    //pagination
    pagination = d3.select("#nowNgoList").select("#pageFoot");
    if(pagination)pagination.remove();
    pagination = d3.select("#nowNgoList").append("div").attr("id","pageFoot");
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
  function listNowNgo(dataSet){
    nodes = dataSet.nodes;
    updateNgoNodes();
    updateNgoList(1);
  }

  function tick() {
    //nodes
    node.attr("transform", function(d) { 
      var temx = Math.max(r,Math.min(width-r,d.x));
      var temy = d.y = Math.max(r,Math.min(height-r,d.y));
      d.x = temx,d.y = temy;
      return "translate(" + temx + "," + temy + ")"; 
      // return "translate(" + d.x + "," + d.y + ")"; 
    });

    //tick links
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    //tick linkText
    linkText.attr("transform", function (d) {
        var xDiff = d.source.x - d.target.x,
            xMid = d.source.x - xDiff / 2;
        var yDiff = d.source.y - d.target.y,
            yMid = d.source.y - yDiff / 2;
        var hyp = Math.sqrt(xDiff * xDiff + yDiff * yDiff),
            cos = xDiff / hyp,
            sin = yDiff / hyp;
        return "matrix(" + 
            [cos, sin, -sin, cos, xMid, yMid] + ")";
    });

  }
  function dbclick(d,i) {
    force.stop();
    console.log("dblclick!");
    d.fixed = false;
    updateNodeID = nodes[i].nodesID;
    dataSetSend = {
        "dataSet": dataSet,  
        "updateNodeID": updateNodeID,
        "id":i
    };
    dataSetSend = JSON.stringify(dataSetSend);
    $.ajax({
      type: "post",
      url: "/extendNode/",
      data: dataSetSend,
      processData: false,
      contentType:"application/json; charset=utf-8",
      dataType: "json",
      success: function(newData) { // data is json,include nodes,edges,property
        dataSet = newData;
        // console.log(dataSet);
        drawKnowGraph(dataSet);
        listNowNgo(dataSet);
      }
    });
  }

  function click(d,i){  // i is the index of node array,shrink node
    if (d3.event.defaultPrevented) return;
    console.log("click!");
    // console.log(d,i);
    function showInfo(){ // show the node's info
    
      var table = d3.select("#Info").select("table");
      if(table)table.remove();
      table =  d3.select("#Info")
                 .append("table")
                 .attr("id","tableNgo")
                 .attr("class","table");
      thead = table.append("thead");
      tbody = table.append("tbody");
      properties = ['name','location','connectionInfo','time','field','province','orgType','description','personCharge','partners','sponsors']
      thead.append("tr")
           .selectAll("th").data(["property","value"]).enter()
           .append("th")
           .text(function(d){
              return d;
            });
      tbodyTr = tbody.selectAll("tr").data(properties).enter()
                     .append("tr");
      temTr = tbodyTr;
      tbodyTh = tbodyTr.append("th").text(function(property){return property;});
      // console.log(tbodyTr);
      tbodyTd = tbodyTr.selectAll("td")
                       .data(function(property){
                          console.log(property,d[property]);
                          value = new Array();
                          value[0] = d[property];
                          return value;
                        })
                       .enter()
                tbodyTd
                       .append("td")
                       .html(function(tdText){
                        return tdText;
                       });
    }
    if(d.nodesLabels == 'ngo')showInfo();
  }
  function mouseOut(d,i){
    tip.hide(d);
  }
  function mouseOver(d,i){
    function showBrief(){
      var st = d.nodesID.toString();
      if(clickListFlag[st] == true){
        clickListFlag[st] = false;
        drawKnowGraph(dataSet);
      }
      tip.show(d);
    }
    showBrief();
  }
  $(window).resize(function() {
    drawKnowGraph(dataSet);
  });
  drawKnowGraph(dataSet);
  listNowNgo(dataSet);
}


