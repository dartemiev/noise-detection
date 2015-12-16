var bodyParser = require("body-parser");
var express = require("express");
var favicon = require("serve-favicon");
var logger = require("morgan");
var http = require("http");
var path = require("path");

var app = module.exports = express();
http.createServer(app).listen(3000);
console.log("Server running at http://localhost:3000/");

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

// view engine setup
app.use(express.static(path.join(__dirname, "public")));
app.use(favicon(path.join(__dirname, "public", "favicon.ico")));
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "jade");

// logging and debug information
app.use(logger("dev"));

app.get("/", require("./routes/index"));