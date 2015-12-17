var mongoose = require("mongoose");
var logger = require("./../../util/logger");

var db = mongoose.connection;
db.on("error", logger.error);
db.once("open", function () {
    // todo
});

// Makes connection asynchronously. Mongoose will queue up database operations and release them when the
// connection is complete.
var url = "mongodb://localhost/tracking";
var options = {};
mongoose.connect(url, options, function (error, result) {
    if (error) {
        logger.error("Connection refused to " + url);
    } else {
        logger.info("Connection successful to: " + url);
    }
});

exports.db = mongoose;