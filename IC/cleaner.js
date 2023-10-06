const Environment = require("./models/environment");
const Robot = require("./models/robot");

// Initialize objects
const cleaner = new Robot();
const environment = new Environment(3, cleaner);

// environment.show_spaces();

spaces = environment.get_spaces();
cleaner.start_dumb(spaces);
// cleaner.start_intelligent(spaces);

// environment.show_spaces();
