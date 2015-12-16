var mongoose = require("mongoose");
var logger = require("./../../util/logger");

var url = "mongodb://localhost/database";
var options = { };

mongoose.connect(url, options, function (error, result) {
    if (error) {
        logger.error("Connection refused to " + url);
        logger.error(error);
    } else {
        logger.info("Connection successful to: " + url);
    }
});

exports.db = mongoose;