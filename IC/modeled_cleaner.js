const Environment = require("./models/environment");
const modeledRobot = require("./models/modeled_robot");

// Initialize objects
const cleaner = new modeledRobot();
const environment = new Environment(3, cleaner);

spaces = environment.get_spaces();

console.log("STARTING ROBOT BASED MODEL:");
cleaner.start_modeled_bot(spaces);
