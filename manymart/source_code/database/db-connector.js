var mysql = require('mysql')

// Create a 'connection pool' using the provided credentials
var pool = mysql.createPool({
    connectionLimit : 10,
    host            : 'classmysql.engr.oregonstate.edu',
    user            : 'cs340_ovenshir',
    password        : 'wVkagwGRBkRU',
    database        : 'cs340_ovenshir'
})

// Export it for use in our application
module.exports.pool = pool;