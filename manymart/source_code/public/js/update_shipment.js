// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for updating entries

// Names and values have been changed to fit the scope of this project.

// Source:
// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%208%20-%20Dynamically%20Updating%20Data


// Get the objects we need to modify
let updateShipmentForm = document.getElementById('update-shipment-form-ajax');

// Modify the objects we need
updateShipmentForm.addEventListener("submit", function (e) {
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputShipmentID = document.getElementById("update-shipment-id");
    let inputShipmentStatus = document.getElementById("update-status");

    // Get the values from the form fields
    let shipmentIDValue = inputShipmentID.value;
    let shipmentStatusValue = inputShipmentStatus.value;

    // Put our data we want to send in a javascript object
    let data = {
        shipment_id: shipmentIDValue,
        shipment_status: shipmentStatusValue,
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "/put-shipment", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            updateRow(xhttp.response, shipmentIDValue);

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));

})


function updateRow(data, shipmentID){
    let parsedData = JSON.parse(data);
    
    let table = document.getElementById("shipments-table");

    for (let i = 0, row; row = table.rows[i]; i++) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       if (table.rows[i].getAttribute("data-value") == shipmentID) {

            // Get the location of the row where we found the matching department ID
            let updateRowIndex = table.getElementsByTagName("tr")[i];

            // Get td of dept value
            let td = updateRowIndex.getElementsByTagName("td")[3];

            // Reassign dept to our value we updated to
            td.innerHTML = parsedData[0].shipment_status; 
       }
    }
}