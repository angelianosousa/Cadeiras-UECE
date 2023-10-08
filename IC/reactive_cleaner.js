const Environment = require("./models/environment");
const reactiveRobot = require("./models/reactive_robot");

// Initialize objects
const cleaner = new reactiveRobot();
const environment = new Environment(3, cleaner);

spaces = environment.get_spaces();

console.log("STARTING REACTIVE ROBOT:");
cleaner.start_reactive_bot(spaces);
