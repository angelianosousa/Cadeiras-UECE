const Environment   = require('./models/environment');
const ReactiveAgent = require('./models/reactive_agent');

// Initialize objects
const cleaner = new ReactiveAgent();

let room_size = 5

const environment = new Environment(room_size);

environment.show_spaces();

spaces = environment.get_spaces();
cleaner.start_clean(spaces);

environment.show_spaces();
