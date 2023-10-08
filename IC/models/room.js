module.exports = class Room {
  constructor(state_room, room_position, spaces) {
    this.state_room = state_room;
    this.position   = room_position;
    this.spaces     = spaces;
  }

  is_clean() {
    return this.state_room == 0;
  }

  clean_state() {
    this.state_room = 0;
  }

  is_spaces_clear() {
    let states_cleaned = [];

    this.spaces.forEach((space) => {
      if (space.is_clean()) {
        states_cleaned.push(0);
      } else {
        states_cleaned.push(1);
      }
    });

    if (states_cleaned.some((state) => state === 1)) {
      return false;
    } else {
      return true;
    }
  }
};
