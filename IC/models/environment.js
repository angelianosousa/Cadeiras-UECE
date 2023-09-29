const Room  = require('./room')
const Math  = require('mathjs');

// 0 For clean
// 1 For dirty

module.exports = class Environment {

  constructor(quantity_spaces, robot, robot_position_column = 0, robot_position_line=0){
    this.quantity_spaces       = quantity_spaces;
    this.spaces                = Math.matrix();
    this.robot_position_column = robot_position_column;
    this.robot_position_line   = robot_position_line;
    this.robot                 = robot;
    this.fill_spaces()
  }  

  fill_spaces(){
    for (let i = 0; i < this.quantity_spaces; i++){
      for (let j = 0; j < this.quantity_spaces; j++){
        this.spaces.set([i, j], new Room(parseInt(Math.random() * 2)));
      }
    }
  }

  show_spaces(){
    this.spaces.forEach(function (space, index) {
      console.log('state room:', space.state_room, 'position:', index);
    });
  }

  get_spaces(){
    return this.spaces;
  }

  get_space(column, line){
    return this.spaces.get([column, line])
  }

}
