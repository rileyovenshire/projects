// Authors: Riley Ovenshire and Triston Osborn

// Code has been altered from the nodejs-starter-app tutorial, for updating entries

// Names and values have been changed to fit the scope of this project.

// Source:
// https://github.com/osu-cs340-ecampus/nodejs-starter-app/tree/main/Step%208%20-%20Dynamically%20Updating%20Data


// Get the objects we need to modify
let updateDepartmentForm = document.getElementById('update-department-form');

// Modify the objects we need
updateDepartmentForm.addEventListener("submit", function (e) {
    // Prevent the form from submitting
    e.preventDefault();

    // Get form fields we need to get data from
    let inputDeptName = document.getElementById("input-deptName-update");
    let inputDeptAmount = document.getElementById("input-deptAmount-update");

    // Get the values from the form fields
    let deptNameValue = inputDeptName.value;
    let deptAmountValue = inputDeptAmount.value;

    // Put our data we want to send in a javascript object
    let data = {
        deptName: deptNameValue,
        deptAmount: deptAmountValue,
    }
    
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "/put-department", true);
    xhttp.setRequestHeader("Content-type", "application/json");

    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 200) {

            // Add the new data to the table
            updateRow(xhttp.response, deptNameValue);

        }
        else if (xhttp.readyState == 4 && xhttp.status != 200) {
            console.log("There was an error with the input.")
        }
    }

    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));

})


function updateRow(data, departmentID){
    let parsedData = JSON.parse(data);
    
    let table = document.getElementById("departments-table");

    for (let i = 0, row; row = table.rows[i]; i++) {
       //iterate through rows
       //rows would be accessed using the "row" variable assigned in the for loop
       if (table.rows[i].getAttribute("data-value") == departmentID) {

            // Get the location of the row where we found the matching department ID
            let updateRowIndex = table.getElementsByTagName("tr")[i];

            // Get td of dept value
            let td = updateRowIndex.getElementsByTagName("td")[2];

            // Reassign dept to our value we updated to
            td.innerHTML = parsedData[0].dept_quantity; 
       }
    }
}