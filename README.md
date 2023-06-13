# PowerSaveMe
## Used API's
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
