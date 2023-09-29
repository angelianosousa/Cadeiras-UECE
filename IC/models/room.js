module.exports = class Room {
  constructor(state_room){
    this.state_room = state_room;
  }

  is_clean(){
    return this.state_room == 0;
  }

  clean_state(){
    this.state_room = 0;
  }
}