
/* GOOGLE CHART INITIALIZATION */
google.charts.load('current', {'packages':['table']});
//google.charts.setOnLoadCallback(FoodTable);

// script root for flask python stuff
$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};



//handles navigation bar tab selection
$(document).ready(function() {

  /* START WEATHER */
  $("#weatherButton").on("click", function() {
    
 
    $.getJSON("http://api.wunderground.com/api/ecbb4b84a1eafec6/conditions/q/TN/Murfreesboro.json", function(parsed_json){

        var location = parsed_json['current_observation']['display_location']['full'],
        time = parsed_json['current_observation']['observation_time'],
        weather = parsed_json['current_observation']['weather'],
        temperature = parsed_json['current_observation']['temperature_string'],
        humidity = parsed_json['current_observation']['relative_humidity'],
        heat_index = parsed_json['current_observation']['heat_index_string'],
        wind = parsed_json['current_observation']['wind_string'],
        icon = parsed_json['current_observation']['icon_url'];
        link = parsed_json['current_observation']['forecast_url'];

    $("#Body").empty();
    $("#Body").append( '<center><br><a href="' + link + '"><img src="'+ icon + '"></a><br><b>' 

          + time + '</b><br>' +

          "Current temperature in <b>" + location + "</b> is: <b>" + temperature + ' </b>and <b>' + weather + '</b><br>' + 

          'Humidity: <b>' + humidity + '</b><br>' +

          'Heat Index: <b>' + heat_index + '</b><br>' +

          'Wind: <b>' + wind + '</b><br>' + '</center>');
        
    });
  });
  /* END WEATHER */
 
 

  $("#calendarButton").on("click", function() {
  });

  $("#transfersButton").on("click", function() {
    $("#Body").empty();
    $("#Body").append( '<form action="/upload-target" class="dropzone dz-clickable"><div class="dz-default dz-message"><span>Drop files here to upload</span></div></form>');
  });



  /*
  $("#kitchenButton").on("click", function() {


  });

  */

});


// empty function to empty elements on the page