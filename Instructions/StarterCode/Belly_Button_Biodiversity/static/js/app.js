function buildMetadata(sample) {
console.log(`inside build meta data ${sample}`);
  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
    // Use d3 to select the panel with id of `#sample-metadata`
    var metadataobj = d3.select("#sample-metadata");
    
    

    d3.json(`/metadata/${sample}`).then((samplemetadata) => {
      //samplemetadata.forEach((metasample) => {
        // metadataobj.html(`Age:${samplemetadata.AGE}`);
        // metadataobj.html(`BBTYPE:${samplemetadata.BBTYPE}`);
        // metadataobj.html(`ETHNICITY:${samplemetadata.ETHNICITY}`);
        // metadataobj.html(`GENDER:${samplemetadata.GENDER}`);
        // metadataobj.html(`LOCATION:${samplemetadata.LOCATION}`);
        metadataobj.html(` <p class="panel-body">Age:${samplemetadata.AGE} <br> BBTYPE:${samplemetadata.BBTYPE} <br> ETHNICITY:${samplemetadata.ETHNICITY} <br> GENDER:${samplemetadata.GENDER} <br> LOCATION:${samplemetadata.LOCATION} <br>  SAMPLEID:${samplemetadata.sample} </p>`);
       //console.log(`Age:${samplemetadata.AGE}`);
      //});

    });
    // Use `.html("") to clear any existing metadata

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
}

function buildCharts(sample) {
  console.log(`inside build charts ${sample}`);

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(`/samples/${sample}`).then(function(sampleadata) {
    console.log(sampleadata);
  
    // @TODO: Build a Bubble Chart using the sample data

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    data = [{
      "labels": sampleadata["otu_ids"],
      "values": sampleadata["sample_values"],
      "type": "pie"}];

      var layout = {
            title: "Pie Chart",
            };

      console.log(`graph data: ${data}`)
      Plotly.newPlot("pie", data, layout);

    });
}

function init() {
  console.log("executing init");
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
 

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    console.log(sampleNames);
    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
     buildCharts(firstSample);
     buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
