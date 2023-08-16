// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for updating entries

// Names and values have been changed to fit the scope of this project.

// Source:
// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%208%20-%20Dynamically%20Updating%20Data


// Get the objects we need to modify
let updateOrderForm = document.getElementById('update-order-form-ajax');

// Modify the objects we need
updateOrderForm.addEventListener("submit", function (e) {
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputOrderID = document.getElementById("select-order-id");
    let inputCustomerID = document.getElementById("select-customer-id");
    let inputShipmentID = document.getElementById("select-shipment-id");
    


    // Get the values from the form fields
    let orderIDValue = inputOrderID.value;
    let customerIDValue = inputCustomerID.value;
    let shipmentIDValue = inputShipmentID.value;

    // Put our data we want to send in a javascript object
    let data = {
        order_id : orderIDValue,
        customer_id : customerIDValue,
        shipment_id : shipmentIDValue,
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "/put-order", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            updateRow(xhttp.response, orderIDValue);

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));

})


function updateRow(data, orderID){
    let parsedData = JSON.parse(data);
    
    let table = document.getElementById("orders-table");

    for (let i = 0, row; row = table.rows[i]; i++) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       if (table.rows[i].getAttribute("data-value") == orderID) {

            // Get the location of the row where we found the matching department ID
            let updateRowIndex = table.getElementsByTagName("tr")[i];

            // Get td of dept value
            let custtd = updateRowIndex.getElementsByTagName("td")[1];
            let shiptd = updateRowIndex.getElementsByTagName("td")[2];

            // Reassign dept to our value we updated to
            custtd.innerHTML = parsedData[0].customer_id; 

            shiptd.innerHTML = parsedData[0].shipment_id; 
       }
    }
}