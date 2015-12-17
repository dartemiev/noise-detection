var bodyParser = require("body-parser");
var express = require("express");
var morgan = require("morgan");
var logger = require("./util/logger");
var db = require("./db/controllers/mongo-db");

var app = express();
app.listen(3000);
app.use(bodyParser());
app.use(morgan("combined", {"stream": logger.stream}));

app.use("/noise", require("./routes/noise.js"));

logger.info("Server \"API\" is running on http://localhost:3000");