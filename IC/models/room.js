module.exports = class Room {
  constructor(state_room, room_position, spaces) {
    this.state_room = state_room;
    this.position = room_position;
    this.spaces = spaces;
  }

  is_clean() {
    return this.state_room == 0;
  }

  clean_state() {
    this.state_room = 0;
  }

  get_room_position() {
    return this.position;
  }

  is_spaces_clear() {
    let clear_states = [];

    this.spaces.forEach((space) => {
      if (space.is_clean()) {
        clear_states.push(0);
      } else {
        clear_states.push(1);
      }
    });

    if (clear_states.some((state) => state === 1)) {
      return false;
    } else {
      return true;
    }
  }
};
