const Environment = require("./models/environment");
const Robot = require("./models/robot");

// Initialize objects
const cleaner = new Robot();
const environment = new Environment(3, cleaner);

spaces = environment.get_spaces();

console.log("STARTING DUMB ROBOT:");
cleaner.start_dumb(spaces, environment);
console.log("=========================================");
