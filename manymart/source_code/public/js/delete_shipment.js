// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for deleting entries

// Names and values have been changed to fit the scope of this project.

// Source:
// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%207%20-%20Dynamically%20Deleting%20Data



function deleteShipment(shipment_id) {
    let data = {
        shipment_id : shipment_id
    };

    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/delete-shipment", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 204) {

            // Delete the new data from the table
            deleteRow(shipment_id);

        }
        else if (xhttp.readyState == 4 && xhttp.status != 204) {
            console.log("There was an error with the input.")
        }
    }
    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
}


function deleteRow(shipment_id){

    let table = document.getElementById("shipments-table");
    for (let i = 0, row; row = table.rows[i]; i++) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       if (table.rows[i].getAttribute("data-value") == shipment_id) {
            table.deleteRow(i);
            break;
       }
    }
}

function deleteDropDownMenu(shipment_id){
    let selectMenu = document.getElementById("update-customer-id");
    for (let i = 0; i < selectMenu.length; i++){
      if (Number(selectMenu.options[i].value) === Number(shipment_id)){
        selectMenu[i].remove();
        break;
      } 
  
    }
  }