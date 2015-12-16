var winston = require("winston");
winston.emitErrs = true;

var logger = new winston.Logger({
    transports: [
        new winston.transports.File({
            level: "info",
            filename: "./logs/all-logs.log",
            handleExceptions: true,
            json: false,
            maxsize: 5242880, //5MB
            maxFiles: 5,
            colorize: false,
            timestamp: true
        }),
        new winston.transports.Console({
            level: "debug",
            handleExceptions: true,
            json: false,
            colorize: true,
            timestamp: true
        })
    ],
    exitOnError: false
});

module.exports = logger;
module.exports.stream = {
    write: function (message, encoding) {
        logger.info(message);
    }
};

module.exports.debug = logger.debug;
module.exports.info = logger.info;
module.exports.warn = logger.warn;
module.exports.error = logger.error;
module.exports.fatal = logger.crit;