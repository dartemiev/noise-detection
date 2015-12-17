var express = require("express");
var schema = require("./../db/models/noise-model");
var logger = require("./../util/logger");

var router = express.Router();

/**
 * Every noise level detected by Raspberry PI has to be registered in system and stored in
 * database. All this data will be queried for analysis, creation graph of noise depends on
 * requested interval and so ever. Raspberry PI detection part has to collect some data
 * (maybe average in given interval) and send it via POST. In general it not good idea to
 * spam for every second (or every detection phase) storing noise level.
 */
router.post("/register", function (request, response) {
    var noise = new schema.Noise();
    noise.level = request.body.level;

    noise.save(function (error) {
        if (error) {
            logger.error(error);
            response.send(500);
            return;
        }

        response.send(200);
    });
});

router.get("/all", function (request, response) {
    var query = schema.Noise.find();
    query.sort("-_added_at");
    query.exec(function (error, results) {
        if (error) {
            logger.error(error);
            response.send(500);
            return;
        }

        response.json(200, results);
    });
});

module.exports = router;
