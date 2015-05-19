//render 
function render(data) {
  var width = 700,
    height = 500,
    root;

  var force = d3.layout.force()
    .linkDistance(80)
    .charge(-120)
    .gravity(.05)
    .size([width, height])
    .on("tick", tick);

  // var svg = d3.select("body").append("svg")
  //   .attr("width", width)
  //   .attr("height", height);
    var svg = d3.select("#graph");

  var link = svg.selectAll(".link"),
    node = svg.selectAll(".node");

  d3.json("/static/js/graph.json", function(error, json) {
    root = json;
    update();
  });

  function update() {
    var nodes = flatten(root),
      links = d3.layout.tree().links(nodes);

    // Restart the force layout.
    force
      .nodes(nodes)
      .links(links)
      .start();

    // Update links.
    link = link.data(links, function(d) {
      return d.target.id;
    });

    link.exit().remove();

    link.enter().insert("line", ".node")
      .attr("class", "link");

    // Update nodes.
    node = node.data(nodes, function(d) {
      return d.id;
    });

    node.exit().remove();

    var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .on("click", click)
      .call(force.drag);

    nodeEnter.append("circle")
      .attr("r", function(d) {
        return Math.sqrt(d.size) / 10 || 4.5;
      });

    nodeEnter.append("text")
      .attr("dy", ".35em")
      .text(function(d) {
        return d.name;
      });

    node.select("circle")
      .style("fill", color);
  }

  function tick() {
    link.attr("x1", function(d) {
        return d.source.x;
      })
      .attr("y1", function(d) {
        return d.source.y;
      })
      .attr("x2", function(d) {
        return d.target.x;
      })
      .attr("y2", function(d) {
        return d.target.y;
      });

    node.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  }
  
  function color(d) {
    return d._children ? "#3182bd" // collapsed package
      : d.children ? "#c6dbef" // expanded package
      : "#fd8d3c"; // leaf node
  }

  // Toggle children on click.
  function click(d) {
    if (d3.event.defaultPrevented) return; // ignore drag
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else {
      d.children = d._children;
      d._children = null;
    }
    update();
  }

  // Returns a list of all nodes under the root.
  function flatten(root) {
    var nodes = [],
      i = 0;
      
    function recurse(node) {
      if (node.children) node.children.forEach(recurse);
      if (!node.id) node.id = ++i;
      nodes.push(node);
    }

    recurse(root);
    return nodes;
  }
}