// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for adding entries

// Names and values have been changed to fit the scope of this project.

// Source:
// // https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%205%20-%20Adding%20New%20Data


// Get the objects we need to modify
let addOrderItemForm = document.getElementById('add-orderitem-form');

// Modify the objects we need
addOrderItemForm.addEventListener("submit", function (e) {

    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputOrderID = document.getElementById("input-order-id");
    let inputItemID = document.getElementById("input-item-id");

    // Get the values from the form fields
    let orderIDValue = inputOrderID.value;
    let itemIDValue = inputItemID.value;

    // Put our data we want to send in a javascript object
    let data = {
        orderID: orderIDValue,
        itemID: itemIDValue
    }

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-orderitem", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            addRowToTable(xhttp.response);

            // Clear the input fields for another transaction
            inputOrderID.value = '';
            inputItemID.value = '';
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
    let currentTable = document.getElementById("orderitems-table");

    // Get the location where we should insert the new row (end of table)
    let newRowIndex = currentTable.rows.length;

    // Get a reference to the new row from the database query (last object)
    let parsedData = JSON.parse(data);
    let newRow = parsedData[parsedData.length - 1]

    // Create a row and 4 cells
    let row = document.createElement("TR");
    let orderItemCell = document.createElement("TD");
    let orderIDCell = document.createElement("TD");
    let itemIDCell = document.createElement("TD");

    // Fill the cells with correct data
    orderItemCell.innerText = newRow.order_item_id;
    orderIDCell.innerText = newRow.order_id;
    itemIDCell.innerText = newRow.item_id;

    deleteCell = document.createElement("button");
    deleteCell.innerHTML = "Delete";
    deleteCell.onclick = function(){
        deleteOrder(newRow.id);
    };

    // Add the cells to the row 
    row.appendChild(orderItemCell);
    row.appendChild(orderIDCell);
    row.appendChild(itemIDCell);

    row.setAttribute('data-value', newRow.order_item_id);

    // Add the row to the table
    currentTable.appendChild(row);

    /* let selectMenu = document.getElementById("input-deptName-update");
    let option = document.createElement("option");
    option.text = newRow.department_name;
    option.value = newRow.department_id;
    selectMenu.add(option); */
}