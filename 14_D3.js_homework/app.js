// D3 Scatterplot Assignment

// Students:
// =========
// Follow your written instructions and create a scatter plot with D3.js.

var svgWidth = 960;
var svgHeight = 500;

var margin = { top: 20, right: 40, bottom: 60, left: 100 };

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3
  .select(".chart")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var chart = svg.append("g");

// Append a div to the body to create tooltips, assign it a class
d3.select(".chart")
  .append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

d3.csv("./data/data.csv", function(err, demoData) {
  if (err) throw err;


  demoData.forEach(function(data) {
    data.abbr = data.abbr;
    data.state = data.state;
    data.lessBachelorDegree = +data.lessBachelorDegree;
    data.obese = +data.obese;
  });

  // Step 1: Create scale functions
  //= =============================
  // Set the domain, and declare x
  var yLinearScale = d3.scaleLinear()
    .range([height, 0]);

  var xLinearScale = d3.scaleLinear()
    .range([0, width]);

  // Step 2: Create axis functions
  //= ============================
  // Declare these variables
  var bottomAxis = d3.axisBottom(xLinearScale);
  var leftAxis = d3.axisLeft(yLinearScale);

  // Step 3: Scale the domain
  //= =======================
  xLinearScale.domain([20, d3.max(demoData, function(data) {
    return +data.lessBachelorDegree;
  })]);
  yLinearScale.domain([0, d3.max(demoData, function(data) {
    return +data.obese * 1.2;
  })]);


  // Step 4: Initialize tooltips
  //= ==========================
  var toolTip = d3.tip()
    .attr("class", "tooltip")
    .offset([80, -60])
    .html(function(data) {
      var state = data.state;
      var education = +data.lessBachelorDegree;
      var obesity = +data.obese;
      return (state + "<br> % < Bachelor's: " + education + "<br> % Obese: " + obesity);
    });

  // // Step 5: call toolTip (this has been done for you)
  // //= ===============================================
  chart.call(toolTip);

  chart.selectAll("circle")
    .data(demoData)
    .enter().append("circle")
      .attr("cx", function(data, index) {
        console.log(data.lessBachelorDegree);
        return xLinearScale(data.lessBachelorDegree);
      })
      .attr("cy", function(data, index) {
        return yLinearScale(data.obese);
      })
      .attr("r", "10")
      .attr("fill", "lightblue")

  //     // Step 6: Use the event listener to create onclick and onmouseout events
  //     //= =====================================================================
      .on("click", function(data) {
        toolTip.show(data);
      })
      // onmouseout event
      .on("mouseout", function(data, index) {
        toolTip.hide(data);
      });


  chart.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

  chart.append("g")
    .call(leftAxis);

  chart.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left + 40)
      .attr("x", 0 - (height / 2))
      .attr("dy", "1em")
      .attr("class", "axisText")
      .text("% Obesity by State");

// Append x-axis labels
  chart.append("text")
    .attr("transform",
          "translate(" + (width / 2) + " ," +
                         (height + margin.top + 30) + ")")
    .attr("class", "axisText")
    .text("% Education Attainment Less than Bachelor Degree by State");
});


