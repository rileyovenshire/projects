// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for updating entries

// Names and values have been changed to fit the scope of this project.

// Source:
// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%208%20-%20Dynamically%20Updating%20Data



// Get the objects we need to modify
let updatePersonForm = document.getElementById('update-item-form');

// Modify the objects we need
updatePersonForm.addEventListener("submit", function (e) {
   
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputItemName = document.getElementById("input-item-update");
    let inputItemPrice = document.getElementById("input-itemPrice-update");
    let inputItemQuant = document.getElementById("input-itemQuant-update");

    // Get the values from the form fields
    let itemNameValue = inputItemName.value;
    let itemPriceValue = inputItemPrice.value;
    let itemQuantityValue = inputItemQuant.value;


    // Put our data we want to send in a javascript object
    let data = {
        itemName: itemNameValue,
        itemPrice: itemPriceValue,
        itemQuantity: itemQuantityValue
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "/put-item", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            updateRow(xhttp.response, itemNameValue);

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));

})


function updateRow(data, itemName){
    let parsedData = JSON.parse(data);
    
    let table = document.getElementById("items-table");

    for (let i = 0, row; row = table.rows[i]; i++) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       if (table.rows[i].getAttribute("data-value") == itemName) {

            // Get the location of the row where we found the matching person ID
            let updateRowIndex = table.getElementsByTagName("tr")[i];

            // Get td of homeworld value
            let priceTD = updateRowIndex.getElementsByTagName("td")[3];
            let quantTD = updateRowIndex.getElementsByTagName("td")[4];

            // Reassign homeworld to our value we updated to
            priceTD.innerHTML = parsedData[0].itemName; 
            quantTD.innerHTML = parsedData[0].itemQuantity; 
       }
    }
}