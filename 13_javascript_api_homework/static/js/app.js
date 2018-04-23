d3.json("/names", function(error, response) {
    // console.log(response);
    var $dropDown = document.getElementById("selSample");

    for (var i = 0; i < response.length; i++) {
        var $option = document.createElement("option");
        $option.innerHTML = response[i];
        $option.setAttribute("value", response[i]);
        $dropDown.appendChild($option);
    };
    });


function getMetadata(sample) {
    d3.json("/metadata/" + sample, function(error, response) {
        if (error) return console.warn(error);

        var keys = Object.keys(response);
        var sampleMetadata = document.getElementById("sample-metadata");
        sampleMetadata.innerHTML = null;
    
        for (var i = 0; i < keys.length; i++) {
            var newLine = document.createElement("p");
            newLine.innerHTML = keys[i] + ": " + response[keys[i]];
            sampleMetadata.appendChild(newLine)

        };
    });

};

function init(sample) {
    getMetadata(sample)
    buildPlot(sample)
    bubblePlot(sample)
};


    
function buildPlot(sample) {
    d3.json("/samples/" + sample, function(error, response) {
        console.log(response);
        var trace1 = {
            values: response[1].sample_values.slice(0, 9),
            labels: response[0].otu_ids.slice(0, 9),
            type: "pie",
        }
    
        var data = [trace1];
    
        var layout = {
            height: 400,
            width: 600,
            title: "Sample Counts for " + sample
        };

        var PIE = document.getElementById('pie');
        Plotly.plot(PIE, data, layout);
    });
}


function bubblePlot(sample) {
    d3.json("/samples/" + sample, function(error, response) {
        console.log(response);
        var trace = {x: response[0]["otu_ids"],
                    y: response[1]["sample_values"],
                    mode: 'markers',
                    marker: {colorscale: 'Electric',
                        color: response[0]["otu_ids"],
                        size: response[1]["sample_values"]},
                    type: "scatter"};

        var bubbleData = [trace];

        var bubbleLayout = {title: 'Sample Values for ' + sample,
                            xaxis: {title: "OTU ID"},
                            showlegend: false,
                            height: 600,

                        };

        Plotly.newPlot('bubblePlot', bubbleData, bubbleLayout);

    });
}


function updatePie(values, labels, sample){
    Plotly.restyle("pie", "values", [values]);
    Plotly.restyle("pie", "labels", [labels]);
    Plotly.relayout("pie", "title", "Sample Counts for " + sample);
    };


function updateBubble(valuesBubble, labelsBubble, sample){
    Plotly.restyle("bubblePlot", "x", [labelsBubble]);
    Plotly.restyle("bubblePlot", "y", [valuesBubble]);
    Plotly.restyle("bubblePlot", "marker.size", [valuesBubble]);
    Plotly.relayout("bubblePlot", "title", "Sample Values for " + sample);
    };


function optionChanged(sample) {
    getMetadata(sample);
    // handle new get request for choice
    d3.json("/samples/" + sample, function(error, response) {
    // error trapping for failed call from Flask
    if (error) return console.warn(error);
  
    var labels = response[0]["otu_ids"].slice(0,9);
    var values = response[1]["sample_values"].slice(0,9);
  
    for (var i = 0; i < 9; i++){
      if (labels[i] == 0){
          labels = labels.slice(0,i)
      };
      if (values[i] == 0){
          values[i] = values.slice(0,i)
      };
    };
  

    // new variables for updateBub function
    var valuesBubble = response[1]['sample_values'];
    var labelsBubble = response[0]['otu_ids'];
  
    // update plots
    updatePie(values, labels, sample);
    updateBubble(valuesBubble, labelsBubble, sample);
    })
  };


init("BB_940")