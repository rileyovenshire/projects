// Authored by Riley Ovenshire and Triston Osborn

// All files have been given citations at the top

// Data has been altered but has been templated based on example code.


// // https://github.com/osu-cs340-ecampus/nodejs-starter-app/main

/*
    SETUP
*/

// Express
var express = require('express');   // We are using the express library for the web server
var app = express();            // We need to instantiate an express object to interact with the server in our code
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

// Static Files
app.use(express.static('public'))

PORT = 32797;                 // Set a port number at the top so it's easy to change in the future

// Database
var db = require('./database/db-connector.js');

// Handlebars
const { engine } = require('express-handlebars');
var exphbs = require('express-handlebars');         // Import express-handlebars
app.engine('.hbs', engine({ extname: ".hbs" }));    // Create an instance of the handlebars engine to process templates
app.set('view engine', '.hbs');                     // Tell express to use handlebars engine whenever it encounters a *.hbs file.

const { json } = require('express');

/*
    ROUTES
*/

// -----------------------------------------------------------------------------------

//Home Page
app.get('/', function (req, res) {
    res.render('index');
});

// ------------------------------------------------------------------------------------

// Orders
app.get('/orders', function (req, res) {
    let query1 = "SELECT * FROM Orders";

    // Dropdown
    let query2 = "SELECT * FROM Customers"

    db.pool.query(query1, function(error, rows, fields){   

        let orders = rows;

        db.pool.query(query2, function(error, rows, fields){
            let customers = rows;
            return res.render('orders', {orders: orders, customers: customers});
        })
    })                                                      
});     

// Add Order
app.post('/add-order', function(req, res) {
    let data = req.body;

    const customer_id = data.customerID
    const order_date = data.orderDate

    // let shipment_id = parseInt(data.shipment_id);
    // if (isNaN(shipment_id))
    // {
    //     shipment_id = 'NULL'
    // }

    query1 = `INSERT INTO Orders (customer_id, shipment_id, order_date) VALUES ('${data.customerID}', '2', '${data.orderDate}}')`;
    // query1 = `CALL CreateOrderWithShipment('${data.customerID}', '${data.orderDate}')`;
    query2 = `UPDATE Orders SET shipment_id = (SELECT MAX(shipment_id) FROM Shipments) WHERE order_id = (SELECT MAX(order_id) FROM Orders)`;
    query3 = `SELECT * FROM Orders`;

    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error)
            res.sendStatus(400);

        }
        else {

            db.pool.query(query2, function(error, rows, fields){

                // If there was an error on the second query, send a 400
                if (error) {
                    
                    console.log(error);
                    res.sendStatus(400);

                }
                else { 
                    db.pool.query(query3, function(error, rows, fields){
                        res.send(rows);
                    })                                   
                    
                }
    })
}})

});




// Delete Order
app.delete('/delete-order', function(req, res, next) {
    
    let data = req.body;

    let orderID = parseInt(data.id);
    
    let deleteOrderShip = `DELETE FROM Shipments where order_id = ?`
    let deleteOrder = `DELETE FROM Orders WHERE order_id = ?;`;

    // Run the 1st query
    db.pool.query(deleteOrder, [orderID], function(error, rows, fields){
        if (error) {

        // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
        console.log(error);
        res.sendStatus(400);
        }

        else
        {
            // Run the second query
            db.pool.query(deleteOrderShip, [orderID], function(error, rows, fields) {

                if (error) {
                    console.log(error);
                    res.sendStatus(400);
                } else {
                    res.sendStatus(204);
                }
            })
        }
})});

// Update Order
app.put('/put-order', function(req,res,next){
    let data = req.body;

    let customerID = parseInt(data.customer_id);
    let shipmentID = parseInt(data.shipment_id);

    let query1 = 'UPDATE Orders SET customer_id = ?, shipment_id = ? WHERE order_id = ?';
    let query2 = 'SELECT * FROM Orders';

          // Run the 1st query
          db.pool.query(query1, [customerID, shipmentID, data.order_id], function(error, rows, fields){
              if (error) {

              // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
              console.log(error);
              res.sendStatus(400);
              }

              // If there was no error, we run our second query and return that data so we can use it to update the people's
              // table on the front-end
              else
              {
                  // Run the second query
                  db.pool.query(query2, function(error, rows, fields) {

                      if (error) {
                          console.log(error);
                          res.sendStatus(400);
                      } else {
                          res.send(rows);
                      }
                  })
              }
  })});

//-----------------------------------------------------------------------------------------------------------------

// Customers
app.get('/customers', function (req, res) {
    let query1 = "SELECT * FROM Customers";

    db.pool.query(query1, function(error, rows, fields){   

        res.render('customers', {customers: rows});   

    })                                                      
});  

// Search for Customers, view their orders

// Add Customer
app.post('/add-customer', function (req, res) {

    let data = req.body;

    query1 = `INSERT INTO Customers (first_name, last_name, email) VALUES ('${data.fname}', '${data.lname}', '${data.email}')`;
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error);
            res.sendStatus(400);

        }
        else {

            query2 = `SELECT * FROM Customers;`;
            db.pool.query(query2, function(error, rows, fields){

                // If there was an error on the second query, send a 400
                if (error) {
                    
                    console.log(error);
                    res.sendStatus(400);

                }
                else {
                    res.send(rows);
                }
            })
        }
    })
});


// Update Customer
app.put('/put-customer', function(req,res,next){
    let data = req.body;

    let queryUpdateCustomer = `UPDATE Customers SET email = ? WHERE Customers.last_name = ?`;
    let selectCustomers = `SELECT * FROM Customers`;
    
        // Run the 1st query
        db.pool.query(queryUpdateCustomer, [data.email, data.last_name], function(error, rows, fields){
            if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error);
            res.sendStatus(400);
            }

            // If there was no error, we run our second query and return that data so we can use it to update the people's
            // table on the front-end
            else
            {
                // Run the second query
                db.pool.query(selectCustomers, function(error, rows, fields) {

                    if (error) {
                        console.log(error);
                        res.sendStatus(400);
                    } else {
                        res.send(rows);
                    }
                })
            }
})});
    


// Delete Customer
app.delete('/delete-customer', function(req, res, next) {
    
    let data = req.body;

    let customerID = parseInt(data.customer_id);


    let query1 = `DELETE FROM Customers WHERE customer_id = ?`;
    let query2 = `DELETE FROM Orders WHERE customer_id = ${customerID}`


    db.pool.query(query2, [customerID], function(error, rows, fields){
        if (error) {

        // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
        console.log(error);
        res.sendStatus(400);
        }

        else
        {
            // Run the second query
            db.pool.query(query1, [customerID], function(error, rows, fields) {

                if (error) {
                    console.log(error);
                    res.sendStatus(400);
                } else {
                    res.sendStatus(204);
                }
            })
        }
})});


//-------------------------------------------------------------------------------------------------------------------------

// Shipments
app.get('/shipments', function (req, res) {
    let query1 = "SELECT * FROM Shipments";

    // Dropdown
    let query2 = "SELECT * from Orders";

    db.pool.query(query1, function(error, rows, fields){   

        let shipments = rows;

        db.pool.query(query2, function(error, rows, fields){
            let orders = rows;
            return res.render('shipments', {shipments: shipments, orders: orders});
        })

    })                                                      
});  

// Add Shipment
app.post('/add-shipment', function (req, res) {

    let data = req.body;

    let shipment_status = parseInt(data.shipment_status);
    if (isNaN(shipment_status))
    {
        shipment_status = 'NULL'
    }

    query1 = `INSERT INTO Shipments (order_id, shipment_date, shipment_status) VALUES ('${data.orderID}', '${data.shipmentDate}', '${data.shipmentStatus}')`;
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error);
            res.sendStatus(400);

        }
        else {

            query2 = `SELECT * FROM Shipments`;
            db.pool.query(query2, function(error, rows, fields){

                // If there was an error on the second query, send a 400
                if (error) {
                    
                    console.log(error);
                    res.sendStatus(400);

                }
                else {
                    res.send(rows);
                }

            })

        }


    })

});

// Update Shipment
app.put('/put-shipment', function(req,res,next){
    let data = req.body;

    let shipment_status = parseInt(data.shipment_status);

    let queryUpdateShipment = `UPDATE Shipments SET shipment_status = ? WHERE Shipments.shipment_id = ?`;
    let selectShipments = `SELECT * FROM Shipments`;
    
        // Run the 1st query
        db.pool.query(queryUpdateShipment, [shipment_status, data.shipment_id], function(error, rows, fields){
            if (error) {

            // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
            console.log(error);
            res.sendStatus(400);
            }

            // If there was no error, we run our second query and return that data so we can use it to update the people's
            // table on the front-end
            else
            {
                // Run the second query
                db.pool.query(selectShipments, function(error, rows, fields) {

                    if (error) {
                        console.log(error);
                        res.sendStatus(400);
                    } else {
                        res.send(rows);
                    }
                })
            }
})});

// Delete Shipment
app.delete('/delete-shipment', function(req, res, next) {
    
    let data = req.body;

    let shipmentID = parseInt(data.shipment_id);
    
    let query1 = `DELETE FROM Shipments WHERE shipment_id = ?`;
    let query2 = `DELETE FROM Orders WHERE shipment_id = ${shipmentID}`


    db.pool.query(query2, [shipmentID], function(error, rows, fields){
        if (error) {

        // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
        console.log(error);
        res.sendStatus(400);
        }

        else
        {
            // Run the second query
            db.pool.query(query1, [shipmentID], function(error, rows, fields) {

                if (error) {
                    console.log(error);
                    res.sendStatus(400);
                } else {
                    res.sendStatus(204);
                }
            })
        }
})});

//---------------------------------------------------------------------------------------------------------------------------

// Departments
app.get('/departments', function (req, res) {
    let query1 = "SELECT * FROM Departments";

    db.pool.query(query1, function(error, rows, fields){   

        res.render('departments', {departments: rows});   

    })                                                      
});  


// Add Department
app.post('/add-department', function (req, res) {

    let data = req.body;

    query1 = `INSERT INTO Departments (department_name, dept_quantity) VALUES ('${data.dName}', '${data.dQuant}')`;
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error);
            res.sendStatus(400);

        }
        else {

            query2 = `SELECT * FROM Departments;`;
            db.pool.query(query2, function(error, rows, fields){

                // If there was an error on the second query, send a 400
                if (error) {

                    console.log(error);
                    res.sendStatus(400);

                }
                else {
                    res.send(rows);
                }

            })

        }


    })

});

// Update Department
app.put('/put-department', function(req,res,next){
    let data = req.body;

    let deptAmount = parseInt(data.deptAmount);
  
    let query1 = `UPDATE Departments SET dept_quantity = ? WHERE Departments.department_name = ?`;
    let query2 = `SELECT * FROM Departments`
  
          // Run the 1st query
          db.pool.query(query1, [deptAmount, data.deptName], function(error, rows, fields){
              if (error) {
  
              // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
              console.log(error);
              res.sendStatus(400);
              }
  
              // If there was no error, we run our second query and return that data so we can use it to update the people's
              // table on the front-end
              else
              {     
                  // Run the second query
                  db.pool.query(query2, function(error, rows, fields) {
                      if (error) {
                          console.log(error);
                          res.sendStatus(400);
                      } else {
                          res.send(rows);
                      }
                  })
              }
  })});

// Delete Department
app.delete('/delete-department', function(req, res, next) {

    let data = req.body;

    let departmentID = parseInt(data.department_id);

    let query1 = `DELETE FROM Departments WHERE department_id = ?`;
    let query2 = `DELETE FROM Items WHERE department_id = ?`


    db.pool.query(query2, [departmentID], function(error, rows, fields){
        if (error) {

        // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
        console.log(error);
        res.sendStatus(400);
        }

        else
        {
            // Run the second query
            db.pool.query(query1, [departmentID], function(error, rows, fields) {

                if (error) {
                    console.log(error);
                    res.sendStatus(400);
                } else {
                    res.sendStatus(204);
                }
            })
        }
})});

//----------------------------------------------------------------------------------------------------------------------------

// Items
app.get('/items', function (req, res) {
    let query1 = "SELECT * FROM Items";

    // Dropdown
    let query2 = "SELECT * FROM Departments";

    db.pool.query(query1, function(error, rows, fields){   

        let items = rows;

        db.pool.query(query2, function(error, rows, fields){

            let departments = rows;
            res.render('items', {items: items, departments: departments});  
        })
    })                                                      
});  

// Add Item
app.post('/add-item', function (req, res) {

    let data = req.body;

    query1 = `INSERT INTO Items (item_name, item_price, item_quantity, department_id) VALUES ('${data.itemName}', '${data.itemPrice}', '${data.itemQuantity}', '${data.deptID}')`;
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error);
            res.sendStatus(400);

        }
        else {

            query2 = `SELECT * FROM Items;`;
            db.pool.query(query2, function(error, rows, fields){

                // If there was an error on the second query, send a 400
                if (error) {
                    
                    console.log(error);
                    res.sendStatus(400);

                }
                else {
                    res.send(rows);
                }

            })

        }


    })

});


// Update Item
app.put('/put-item', function(req,res,next){
    let data = req.body;

    let price = parseInt(data.itemPrice);
    let quant = parseInt(data.itemQuantity);

    let query1 = 'UPDATE Items SET item_price = ?, item_quantity = ? WHERE item_name = ?';
    let query2 = 'SELECT * FROM Items';

          // Run the 1st query
          db.pool.query(query1, [price, quant, data.itemName], function(error, rows, fields){
              if (error) {

              // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
              console.log(error);
              res.sendStatus(400);
              }

              // If there was no error, we run our second query and return that data so we can use it to update the people's
              // table on the front-end
              else
              {
                  // Run the second query
                  db.pool.query(query2, function(error, rows, fields) {

                      if (error) {
                          console.log(error);
                          res.sendStatus(400);
                      } else {
                          res.send(rows);
                      }
                  })
              }
  })});

// Delete Item
app.delete('/delete-item', function(req, res, next) {
    
    let data = req.body;

    let item_id = parseInt(data.item_id);
    
    let query1 = `DELETE FROM Items WHERE item_id = ?`;

    db.pool.query(query1, [item_id], function(error, rows, fields){
        if (error) {

        // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
        console.log(error);
        res.sendStatus(400);
        }

        else
        {
            res.sendStatus(204);
        }
})});


//-----------------------------------------------------------------------

// Order Items
app.get('/orderitems', function (req, res) {
    let query = `
        SELECT oi.order_item_id, o.order_id, i.item_id
        FROM OrderItems oi
        INNER JOIN Orders o ON oi.order_id = o.order_id
        INNER JOIN Items i ON oi.item_id = i.item_id
    `;

    db.pool.query(query, function(error, rows, fields){   
        if (error) {
            console.error(error);
            return res.status(500).json({ error: 'Error fetching data' });
        }

        let orderitems = rows;
        
        // Render the orderitems page and pass the data
        return res.render('orderitems', { orderitems: orderitems });
    });
});

// Add to OrderItems when Order is created
app.post('/add-orderitem', function (req, res) {

    let data = req.body;

    query1 = `INSERT INTO OrderItems (order_id, item_id) VALUES ('${data.orderID}', '${data.itemID}')`;
    db.pool.query(query1, function (error, rows, fields) {

        if (error) {

            console.log(error);
            res.sendStatus(400);

        }
        else {

            query2 = `SELECT * FROM OrderItems;`;
            db.pool.query(query2, function(error, rows, fields){

                // If there was an error on the second query, send a 400
                if (error) {

                    console.log(error);
                    res.sendStatus(400);

                }
                else {
                    res.send(rows);
                }

            })

        }


    })

});

app.delete('/delete-orderitem', function(req, res, next) {
    
    let data = req.body;

    let order_item_id = parseInt(data.order_item_id);
    
    let query1 = `DELETE FROM OrderItems WHERE order_item_id = ?`;

    db.pool.query(query1, [order_item_id], function(error, rows, fields){
        if (error) {

        // Log the error to the terminal so we know what went wrong, and send the visitor an HTTP response 400 indicating it was a bad request.
        console.log(error);
        res.sendStatus(400);
        }

        else
        {
            res.sendStatus(204);
        }
})});


// -----------------------------------------------------------------------

/*
    LISTENER
*/
app.listen(PORT, function () {            // This is the basic syntax for what is called the 'listener' which receives incoming requests on the specified PORT.
    console.log('Express started on http://localhost:' + PORT + '; press Ctrl-C to terminate.')
});