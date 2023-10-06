const Math = require("mathjs");

module.exports = class Robot {
  constructor() {
    this.space_counting = 0;
    this.room_states = [];
  }

  start_dumb(spaces) {
    const win_points = () => this.win_points();
    const lose_points = () => this.lose_points();

    let start = true;

    /**
     * [0,0][0,1][0,2]
     * [1,0][1,1][1,2]
     * [2,0][2,1][2,2]
     */

    while (start) {
      spaces.forEach(function (space) {
        if (space.is_spaces_clear()) {
          start = false;
        }
      });

      let room = [];

      for (let i = 0; i < 3; i++) {
        room[i] = [];
        for (let j = 0; j < 3; j++) {
          room[i][j] = spaces.get([i, j]).state_room;
        }
      }

      console.log(room);

      const randomX = Math.floor(Math.random() * 3); //multiplica pelo numero da matriz
      const randomY = Math.floor(Math.random() * 3);

      const currentRoom = spaces.get([randomX, randomY]);

      console.log(spaces.get([randomX, randomY]).get_room_position());

      if (currentRoom.is_clean()) {
        console.log("Space already clean");
        lose_points();
      } else {
        console.log("Cleaning...");
        currentRoom.clean_state();
        win_points();
      }
    }

    console.log("Total points: ", this.space_counting);
  }

  // start_intelligent(spaces) {
  //   const win_points = () => this.win_points();
  //   const lose_points = () => this.lose_points();
  //   const room_states = () => this.get_room_spaces();

  //   const set_room_states = (state) => this.room_states.push(state);

  //   spaces.forEach(function (space) {
  //     set_room_states(space.get_room_position());

  //     if (space.is_clean()) {
  //       console.log("Space clean");
  //       lose_points();
  //     } else {
  //       console.log("Cleaning...");
  //       space.clean_state();
  //       win_points();
  //     }

  //     console.log("Room Stats: ", room_states());
  //   });
  // }

  win_points() {
    this.space_counting += 1;
  }

  lose_points() {
    this.space_counting -= 1;
  }

  get_room_spaces() {
    return this.room_states;
  }
};
