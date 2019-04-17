

// Define SVG area dimensions
var svgWidth = 960;
var svgHeight = 660;

// Define the chart's margins as an object
var chartMargin = {
        top: 20,
        right: 20,
        bottom: 80,
        left: 40
};

// Define dimensions of the chart area
var width = svgWidth - chartMargin.left - chartMargin.right;
var height = svgHeight - chartMargin.top - chartMargin.bottom;


var svg_object = d3.select("#scatter")
                    .append("svg")
                    .attr("height", svgHeight)
                    .attr("width", svgWidth);

var chartGroup = svg_object.append("g")
        .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);


d3.csv("data/data.csv", function(stateDemo) {
 
  stateDemo.forEach(function(d) {
    d.poverty = +d.poverty;
    d.healthcare = +d.healthcare;
  });

  var xLinearScale = d3.scaleLinear()
          .domain([5, d3.max(stateDemo, d => d.poverty)])
          .range([0, width]);

  var yLinearScale = d3.scaleLinear()
          .domain([3, d3.max(stateDemo, d => d.healthcare)])
          .range([height, 0]);

  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  chartGroup.append("g")
          .attr("transform", `translate(0, ${height})`)
          .call(bottomAxis);

  chartGroup.append("g")
          .call(leftAxis);

  var circles = chartGroup.selectAll("circle")
            .data(stateDemo)
            .enter()
            .append("circle")
            .attr("cx", d => xLinearScale(d.poverty))
            .attr("cy", d => yLinearScale(d.healthcare))
            .attr("r", "15")
            .attr("fill", "lightblue")
            .attr("opacity", "1")
            .classed("add_labels",true)
            
  var labels =  chartGroup.selectAll("add_labels")
            .data(stateDemo)
            .enter()
            .append("text")
            .attr("x", d => xLinearScale(d.poverty))
            .attr("y",d => yLinearScale(d.healthcare))
            .text(function(d){return d.abbr})
            .attr("text-anchor","middle")
            .attr("alignment-baseline","middle")
            .attr("stroke","#a3a3a3");

    // Create axes labels
    chartGroup.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - chartMargin.left - 5 )
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    .attr("class", "axisText")
    .text("Lacks Healthcare (%)");

  chartGroup.append("text")
    .attr("transform", `translate(${width / 2}, ${height + chartMargin.top + 20})`)
    .attr("class", "axisText")
    .text("In Poverty (%)");

})
 
   










