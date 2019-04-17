// from data.js
var tableData = data;

console.log(tableData);

// YOUR CODE HERE!
// Select the submit button
var filter_button = d3.select("#filter-btn");

filter_button.on("click", function () {

     // Prevent the page from refreshing
    d3.event.preventDefault();

    // grabs the input tag with id datetime
    var dateInput = d3.select("#datetime");

    // gets the vale of the input entered
    var dateInput_value = dateInput.property("value");

    //filters the data from the data.js by the date entered in the form once button is clicked
    var filteredInput = tableData.filter(tableData => tableData.datetime === dateInput_value);

    console.log(filteredInput)
    
    // create arrays to hold the filtered data
    var date_output = []
    var city_output = []
    var state_output = []
    var country_output = []
    var shape_output = []
    var duration_output = []
    var comments_output = []

    //loops throuhg the filtered data to place in each array for assinging to html td's
    for (index in filteredInput) {
            // console.log("this is the start of the key",key);
            // console.log("--------------------------------------");
            // console.log("this is the start of the data",filteredInput[key]['city']);
            // console.log("--------------------------------------");

            date_output.push(filteredInput[index]['datetime']);
            city_output.push(filteredInput[index]['city']);
            state_output.push(filteredInput[index]['state']);
            country_output.push(filteredInput[index]['country']);
            shape_output.push(filteredInput[index]['shape']);
            duration_output.push(filteredInput[index]['durationMinutes']);
            comments_output.push(filteredInput[index]['comments']);

        }

    //loops through all dates that match input and appends to table
    for (index in date_output) {
        
        //selects the th with class table-head and assing a table row with id of output and index
        d3.select(".table-body").append("tr").attr("id",`output${index}`);
                
                //selects the table row with that output and index and append td for each record in those arrays
                d3.select(`#output${index}`).append("td").text(date_output[index]);
                d3.select(`#output${index}`).append("td").text(city_output[index]);
                d3.select(`#output${index}`).append("td").text(state_output[index]);
                d3.select(`#output${index}`).append("td").text(country_output[index]);
                d3.select(`#output${index}`).append("td").text(shape_output[index]);
                d3.select(`#output${index}`).append("td").text(duration_output[index]);
                d3.select(`#output${index}`).append("td").text(comments_output[index]);
       
    }

    window.onload = function() {
        document.getElementById("my_audio").play();
    }

});


