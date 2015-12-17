var mongoose = require("mongoose");
var Schema = mongoose.Schema;

var Noise = new Schema({
    level: {
        type: Number,
        required: true
    },
    added_at: {
        type: Date,
        default: Date.now
    }
});

exports.Noise = mongoose.model("Noise", Noise);