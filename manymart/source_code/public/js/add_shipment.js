// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for adding entries

// Names and values have been changed to fit the scope of this project.

// Source:
// // https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%205%20-%20Adding%20New%20Data


// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%205%20-%20Adding%20New%20Data

// Get the objects we need to modify
let addShipmentForm = document.getElementById('add-shipment-form-ajax');

// Modify the objects we need
addShipmentForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputOrderID = document.getElementById("select-order");
    let inputShipmentDate = document.getElementById("input-shipment-date")

    // Get the values from the form fields
    let orderIDValue = inputOrderID.value;
    let shipmentDateValue = inputShipmentDate.value;


    // Put our data we want to send in a javascript object
    let data = {
        orderID : orderIDValue,
        shipmentDate : shipmentDateValue,
        shipmentStatus : 1,
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-shipment", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            addRowToTable(xhttp.response);

            // Clear the input fields for another transaction
            inputOrderID.value = '';
            inputShipmentDate = '';

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));

})


// Creates a single row from an Object representing a single record
addRowToTable = (data) => {

    // Get a reference to the current table on the page and clear it out.
    let currentTable = document.getElementById("shipments-table");

    // Get the location where we should insert the new row (end of table)
    let newRowIndex = currentTable.rows.length;

    // Get a reference to the new row from the database query (last object)
    let parsedData = JSON.parse(data);
    let newRow = parsedData[parsedData.length - 1]

    // Create a row and 4 cells
    let row = document.createElement("TR");
    let shipmentIDCell = document.createElement("TD");
    let orderIDCell = document.createElement("TD");
    let shipmentDateCell = document.createElement("TD");
    let shipmentStatusCell = document.createElement("TD");
    let deleteCell = document.createElement("TD");

    // Fill the cells with correct data
    shipmentIDCell.innerText = newRow.shipment_id;
    orderIDCell.innerText = newRow.order_id;
    shipmentDateCell.innerText = newRow.shipment_date;
    shipmentStatusCell.innerText = newRow.shipment_status;
    deleteCell = document.createElement("button");
    deleteCell.innerHTML = "Delete";
    deleteCell.onclick = function(){
        deleteShipment(newRow.shipment_id);
    };

    // Add the cells to the row 
    row.appendChild(shipmentIDCell);
    row.appendChild(orderIDCell);
    row.appendChild(shipmentDateCell);
    row.appendChild(shipmentStatusCell);
    row.appendChild(deleteCell);

    // Add a row attribute so the deleteRow function can find a newly added row
    row.setAttribute('data-value', newRow.shipment_id)
    
    // Add the row to the table
    currentTable.appendChild(row);
}