# PowerSaveMe
## Used API's
### Electricy Prices
First the free API from https://www.elprisetjustnu.se/elpris-api was found. It returns a json which includes the price for KwH in SEK and EUR and the time(hourly). To receive the data in
Google Data, Google Sheets was used, to receive the information through the API and do some basic processing. The code for the Google Sheets that receives the API and process the data is 
```function fetchDataFromAPI() {
  var url = 'https://www.elprisetjustnu.se/api/v1/prices/2023/06-12_SE1.json';
  
  var response = UrlFetchApp.fetch(url);
  var data = JSON.parse(response.getContentText());
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Clear existing data in the sheet
  sheet.clear();
  
  // Set column headers
  var headers = Object.keys(data[0]);
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  
  // Populate the data in the sheet
  var values = data.map(function(rowData) {
    // Convert the date in the third column
    var date = new Date(rowData.time_start); // Assuming the date is stored in the 'time_start' property
    var formattedDate = formatDate(date); // Use the formatDate function from the previous example
    
    // Replace the original date with the formatted date
    rowData.time_start = formattedDate;
    
    return Object.values(rowData);
  });
  
  sheet.getRange(2, 1, values.length, values[0].length).setValues(values);
}

// This code makes the date to ISO 8601 format.
function formatDate(date) {
  var year = date.getFullYear();
  var month = ("0" + (date.getMonth() + 1)).slice(-2);
  var day = ("0" + date.getDate()).slice(-2);
  
  var hours = ("0" + date.getHours()).slice(-2);
  var minutes = ("0" + date.getMinutes()).slice(-2);
  var seconds = ("0" + date.getSeconds()).slice(-2);
  
  var formattedDate = year + "-" + month + "-" + day + "T" + hours + ":" + minutes + ":" + seconds;
  
  return formattedDate;
}
```
Later the Sheet was imported to the Google Data and a chart was made from it.
### Geolocation API

To get Users longitude and latitude a geolocation API is needed, for now i am using a free API which is limited to 2500 calls/day which is more that enough for right now. 
I am sending a requst with City and Country name and getting back location. 
```
function geocodeCity(cityName, apiKey) {
  var api_url = 'https://api.opencagedata.com/geocode/v1/json';

  var query = encodeURIComponent(cityName);
  var request_url = api_url +
    '?' +
    'key=' + apiKey +
    '&q=' + query;

  var response = UrlFetchApp.fetch(request_url);
  var data = JSON.parse(response.getContentText());

  if (data.status.code === 200) {
    var latitude = data.results[0].geometry.lat;
    var longitude = data.results[0].geometry.lng;
    return { latitude: latitude, longitude: longitude };
  } else {
    throw new Error('Failed to geocode city.');
  }
}

// Example usage
var city = 'Luleå, Sweden';
var apiKey = '8059d5c7a5284da497c2979a305070fb'; // Replace with your OpenCage API key

try {
  var coordinates = geocodeCity(city, apiKey);
  console.log('Latitude: ' + coordinates.latitude);
  console.log('Longitude: ' + coordinates.longitude);
} catch (error) {
  console.error(error);
}

```
### Temperature Forecast API and extraction. To retrieve the temperature the SMHI api is used and code looks like that 
```
var url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/'+lon+'/lat/'+lat+'/data.json';

var response = UrlFetchApp.fetch(url);
var data = JSON.parse(response.getContentText());

const currentTime = new Date(); // Current time
const nextTwoDays = currentTime.getTime() + (2 * 24 * 60 * 60 * 1000); // Time for next two days

const nextTwoDaysData = data.timeSeries.reduce((result, entry) => {
  const validTime = new Date(entry.validTime);
  if (validTime.getTime() <= nextTwoDays) {
    const temperature = entry.parameters.find(param => param.name === "t").values[0];
    result.push({
      time: entry.validTime,
      temperature: temperature
    });
  }
  return result;
}, []);

console.log(nextTwoDaysData)

const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const lastRow = sheet.getLastRow();

  // Clear previous data (excluding the row titles)
  if (lastRow > 1) {
    sheet.getRange(2, 1, lastRow - 1, 2).clearContent();
  }

  // Set the row titles
  sheet.getRange("A1").setValue("Time");
  sheet.getRange("B1").setValue("Temperature");

  // Write the data to the sheet
  for (let i = 0; i < nextTwoDaysData.length; i++) {
    const { time, temperature } = nextTwoDaysData[i];

    sheet.getRange(i + 2, 1).setValue(time);
    sheet.getRange(i + 2, 2).setValue(temperature);
  }
```
