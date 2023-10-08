const Room = require("./room");
const Math = require("mathjs");

// 0 For clean
// 1 For dirty

module.exports = class Environment {
  constructor(
    quantity_spaces,
    robot,
    robot_position_column = 0,
    robot_position_line = 0
  ) {
    this.quantity_spaces       = quantity_spaces;
    this.spaces                = Math.matrix();
    this.robot_position_column = robot_position_column;
    this.robot_position_line   = robot_position_line;
    this.robot                 = robot;
    this.fill_spaces();
  }

  fill_spaces() {
    for (let line = 0; line < this.quantity_spaces; line++) {
      for (let column = 0; column < this.quantity_spaces; column++) {
        const state_room = parseInt(Math.random() * 2);
        this.spaces.set([line, column], new Room(state_room, [line, column], this.spaces));
      }
    }
  }

  get_spaces() {
    return this.spaces;
  }
};
