// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for adding entries

// Names and values have been changed to fit the scope of this project.

// Source:
// // https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%205%20-%20Adding%20New%20Data


// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%205%20-%20Adding%20New%20Data

let addItemForm = document.getElementById('add-item-form-ajax');

// Modify the objects we need
addItemForm.addEventListener("submit", function (e) {
    
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputItemName = document.getElementById("input-item-name");
    let inputItemPrice = document.getElementById("input-item-price");
    let inputItemQuantity = document.getElementById("input-item-quantity")
    let itemDept = document.getElementById("select-item-dept")

    // Get the values from the form fields
    let itemNameValue = inputItemName.value;
    let itemPriceValue = inputItemPrice.value;
    let itemQuantityValue = inputItemQuantity.value;
    let deptIDValue = itemDept.value;

    // Put our data we want to send in a javascript object
    let data = {
        itemName: itemNameValue,
        itemPrice: itemPriceValue,
        itemQuantity: itemQuantityValue,
        deptID: deptIDValue,
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/add-item", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            addRowToTable(xhttp.response);

            // Clear the input fields for another transaction
            inputItemName.value = '';
            inputItemPrice.value = '';
            inputItemQuantity.value = '';
            itemDept.value = '';

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
    let currentTable = document.getElementById("items-table");

    // Get the location where we should insert the new row (end of table)
    let newRowIndex = currentTable.rows.length;

    // Get a reference to the new row from the database query (last object)
    let parsedData = JSON.parse(data);
    let newRow = parsedData[parsedData.length - 1]

    // Create a row and 4 cells
    let row = document.createElement("TR");
    let itemIDCell = document.createElement("TD");
    let itemNameCell = document.createElement("TD");
    let itemPriceCell = document.createElement("TD");
    let itemQuantityCell = document.createElement("TD");
    let deptIDCell = document.createElement("TD");
    let deleteCell = document.createElement("TD");

    // Fill the cells with correct data
    itemIDCell.innerText = newRow.item_id;
    itemNameCell.innerText = newRow.item_name;
    itemPriceCell.innerText = newRow.item_price;
    itemQuantityCell.innerText = newRow.item_quantity;
    deptIDCell.innerText = newRow.department_id;
    deleteCell = document.createElement("button");
    deleteCell.innerHTML = "Delete";
    deleteCell.onclick = function(){
        deleteItem(newRow.item_id);
    };

    // Add the cells to the row 
    row.appendChild(itemIDCell);
    row.appendChild(itemNameCell);
    row.appendChild(itemPriceCell);
    row.appendChild(itemQuantityCell);
    row.appendChild(deptIDCell);
    row.appendChild(deleteCell)

    // Add a row attribute so the deleteRow function can find a newly added row
    row.setAttribute('data-value', newRow.item_id)
    
    // Add the row to the table
    currentTable.appendChild(row);

    let selectMenu = document.getElementById("input-item-update");
    let option = document.createElement("option");
    option.text = newRow.itemName;
    option.value = newRow.id;
    selectMenu.add(option);

}