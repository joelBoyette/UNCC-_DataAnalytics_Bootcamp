function buildMetadata(sample) {

    var base_url = "/metadata/";
    var full_path = base_url + sample;

      d3.json(full_path).then(function(response){

        // assign id to variable that clears the html for next set of data
        var metadata = d3.select("#sample-metadata").html("")

       //loops through each metadata and appends a paragraph to each key/value
        Object.entries(response).forEach(([key, value]) => {

          metadata.append("p").text(`${key}: ${value}`)
        });

      })
    }

    function gaugeChart(sample) {
      
      var base_url = "/metadata/";
      var full_path = base_url + sample;

      d3.json(full_path).then(function(response){
    
      //plot the gauge chart
      // Enter a level between 0 and 9
      var level = response.WFREQ;

      // Trig to calc meter point
      var degrees = 9 - level,
      radius = .5;
      var radians = degrees * Math.PI / 9;
      var x = radius * Math.cos(radians);
      var y = radius * Math.sin(radians);

      // Path: may have to change to create a better triangle
      var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
      pathX = String(x),
      space = ' ',
      pathY = String(y),
      pathEnd = ' Z';
      var path = mainPath.concat(pathX,space,pathY,pathEnd);

      var data = [
            { type: 'scatter',
              x: [0], y:[0],
              marker: {size: 28 , color:'850000'},
              showlegend: false,
              name: "Belly Button Washing Frequency",
              text: level,
              hoverinfo: 'text+name',
            },
            { values: [50/9,50/9,50/9,50/9,50/9,50/9,50/9,50/9,50/9,50],
              rotation: 90,
              text: ['8-9', '7-8', '6-7', '5-6',
                        '4-5', '3-4', '2-3', '1-2', '0-1'],
              textinfo: 'text',
              textposition:'inside',
              marker: {colors:['#FF00FF','#FF0080','#FF0000','#FF8000','#FFF00',
                                '#80FF00','#00FF00','#00FF80','#00FFFF','rgba(255, 255, 255, 0)'
                      ]},
              labels: ['8-9', '7-8', '6-7', '5-6',
                       '4-5', '3-4', '2-3', '1-2', '0-1'],
              hoverinfo: 'label',
              hole: .5,
              type: 'pie',
              showlegend: false
          }
        ];

        var layout = {
          shapes:[
            { type: 'path',
              path: path,
              fillcolor: '850000',
              line: {color: '850000'}
            }],
          title: "Belly Button Washing Frequency <br\> Scrubs Per Week",
          height: 500,
          width: 800,
          xaxis: {zeroline:false, showticklabels:false,
                     showgrid: false, range: [-1, 1]},
          yaxis: {zeroline:false, showticklabels:false,
                     showgrid: false, range: [-1, 1]}
        };

        Plotly.newPlot('gauge', data, layout);

      })   
}

function buildCharts(sample) {

    var base_url = "/samples/";
    var full_path = base_url + sample;

    d3.json(full_path).then(function(response){
      
      //plot the bubble chart
      var trace1_bubble = {
        x: response.otu_ids,
        y: response.sample_values,
        text: response.otu_labels,
        mode:'markers',
        marker:{size: response.sample_values,
                color: response.otu_ids
              }
      }

      var data_bubble = [trace1_bubble];
      var layout_bubble = {
                          xaxis: {title: 'OTU ID'}
                          }
      Plotly.newPlot("bubble",data_bubble,layout_bubble);

      //plot the pie chart
      var trace1_pie = {
        values: response.sample_values.slice(0,10),
        labels:  response.otu_ids.slice(0,10),
        type:'pie',
        hovertext : response.otu_labels.slice(0,10)
      };

      var data_pie = [trace1_pie];
      var layout_pie = {height:400,width:500};
      Plotly.newPlot("pie",data_pie,layout_pie)

      })

}





function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector.append("option")
              .text(sample)
              .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
    gaugeChart(firstSample);
    
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
  gaugeChart(newSample);
}

// Initialize the dashboard
init();
