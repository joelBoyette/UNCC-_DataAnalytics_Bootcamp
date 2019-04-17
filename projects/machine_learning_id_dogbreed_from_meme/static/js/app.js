

//route from app.py (where the json data comes from)
const pythonUrl = "/dog_list";

//reads the json data from the route and then process the function
d3.json(pythonUrl).then(function(data) {

    //convert the json data into an arrayc that can be iterated over
    pythonData = data[0];

    var dog_predictions_dict = {};
    var dog_predictions_list = [];

    for (var i = 0; i < pythonData['Image'].length; i++)
    {   
        dog_predictions_dict = {Image: pythonData['Image'][i],
                                Prediction: pythonData['Prediction'][i],
                                Prediction_Rank: pythonData['Prediction_Rank'][i]};
       
        dog_predictions_list.push(dog_predictions_dict);
    }

    //converts the dog predictions into a unique list of dogs
    let dog_unique = [...new Set(pythonData['Prediction'])]; 

    //element for drop down box
    var select = document.getElementById("example-select");
    
    //creates drop down list
    for(index in dog_unique) {
        select.options[select.options.length] = new Option(dog_unique[index], index);
        }

    // Select the submit button
    var filter_button = d3.select("#filter-btn");

    filter_button.on("click", function () {
       
        
        // Prevent the page from refreshing
       d3.event.preventDefault();
   
       // grabs the input tag with id dog_type
       var dogInput_value = d3.select("#example-select option:checked").text();
   
       //filters the data from the data.js by the dog entered in the form once button is clicked
       var filteredInput = dog_predictions_list.filter(dog_predictions_list => dog_predictions_list.Prediction === dogInput_value);
       
       console.log('input value',dogInput_value);
       console.log('filtered input',filteredInput);
       
       // create arrays to hold the filtered data
       var dog_output = []

       //loops throuhg the filtered data to place in each array for assinging to html td's
       for (index in filteredInput) {
               dog_output.push(filteredInput[index]['Image']);
           }
        
        console.log(dog_output)

        var data= d3.selectAll("#images").append("div").classed("dog_image", true)
        
        data.selectAll(".dog_image").data(dog_output).enter()
        .append("a").attr("id",function (d,i) {return `output${(i)}`;})
        .attr("href",function (d) {return d;})
        .append("img").attr("src", function (d) {return d;});
  
   });


});

