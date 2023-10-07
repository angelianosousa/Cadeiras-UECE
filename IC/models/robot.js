const Math = require("mathjs");

module.exports = class Robot {
  constructor() {
    this.space_counting = 0;
    this.room_states = [];
  }

  async start_dumb(spaces, environment) {
    const start_intelligent = (spacesParam) =>
      this.start_intelligent(spacesParam);
    const win_points = () => this.win_points();
    const lose_points = () => this.lose_points();
    const get_points = () => this.space_counting;

    /**
     * [0,0][0,1][0,2]
     * [1,0][1,1][1,2]
     * [2,0][2,1][2,2]
     */

    let start = true;
    let room_size = 3;
    let robotPositionX = 0;
    let robotPositionY = 0;

    while (start) {
      // Check if room was cleaned
      spaces.forEach(function (space) {
        if (space.is_spaces_clear() && start) {
          console.log("All Cleaned!!");

          console.log("Total points: ", get_points());

          start = false;
        }
      });

      if (!start) break;

      // Await for a second
      // await new Promise((r) => setTimeout(r, 1000));

      // Variables
      let findOtherRoom = false;

      let room = [];

      let initialRobotPositionX = robotPositionX;
      let initialRobotPositionY = robotPositionY;

      // Print room
      for (let i = 0; i < room_size; i++) {
        room[i] = [];
        for (let j = 0; j < room_size; j++) {
          room[i][j] = spaces.get([i, j]).state_room;
        }
      }
      console.log(room);

      const verifyIfRoomIsAble = () => {
        if (
          robotPositionX > room_size - 1 ||
          robotPositionX < 0 ||
          robotPositionY > room_size - 1 ||
          robotPositionY < 0
        ) {
          return false;
        }

        return true;
      };

      // Decide how direction to go
      const randomMovement = Math.floor(Math.random() * 4);
      switch (randomMovement) {
        case 0:
          // Move UP
          console.log("Moving to UP");
          robotPositionX--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 1:
          // Move DOWN
          console.log("Moving to DOWN");
          robotPositionX++;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 2:
          // Move RIGHT
          console.log("Moving to RIGHT");
          robotPositionY++;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 3:
          // Move LEFT
          console.log("Moving to LEFT");
          robotPositionY--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;

        default:
          // Move UP
          console.log("Moving to UP");
          robotPositionX--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
      }

      // Cleaner action
      if (findOtherRoom) {
        console.log("===========================================");
        console.log("Wall finded! Calculating other route...");
        console.log("===========================================");

        robotPositionX = initialRobotPositionX;
        robotPositionY = initialRobotPositionY;
      } else {
        const currentRoom = spaces.get([robotPositionX, robotPositionY]);

        console.log(
          spaces.get([robotPositionX, robotPositionY]).get_room_position()
        );

        if (currentRoom.is_clean()) {
          console.log("Space already clean");
          lose_points();
        } else {
          console.log("Cleaning...");
          currentRoom.clean_state();
          win_points();
        }
      }
    }

    console.log("STARTING INTELLIGENT ROBOT:");
    start_intelligent(environment.get_spaces_backup());
    console.log("=========================================");
  }

  async start_intelligent(spaces) {
    this.space_counting = 0;
    const win_points = () => this.win_points();
    const lose_points = () => this.lose_points();
    const get_points = () => this.space_counting;

    let start = true;
    let room_size = 3;
    let robotPositionX = 0;
    let robotPositionY = 0;
    let robot_states = [];

    while (start) {
      console.log("States: ", robot_states);

      // Check if room was cleaned
      spaces.forEach(function (space) {
        if (space.is_spaces_clear() && start) {
          console.log("All Cleaned!!");

          console.log("Total points: ", get_points());

          start = false;
        }
      });

      if (!start) break;

      // Await for a second
      // await new Promise((r) => setTimeout(r, 1000));

      // Variables
      let findOtherRoom = false;

      let room = [];

      let initialRobotPositionX = robotPositionX;
      let initialRobotPositionY = robotPositionY;

      // Print room
      for (let i = 0; i < room_size; i++) {
        room[i] = [];
        for (let j = 0; j < room_size; j++) {
          room[i][j] = spaces.get([i, j]).state_room;
        }
      }
      console.log("Room: ", room);

      /**
       * [0,0][0,1][0,2]
       * [1,0][1,1][1,2]
       * [2,0][2,1][2,2]
       */

      const verifyIfRoomIsAble = () => {
        const hasState = robot_states.some((states) => {
          return (
            states &&
            states[0] === robotPositionX &&
            states[1] === robotPositionY
          );
        });

        const statesPossibles = [];
        statesPossibles.push([robotPositionX++, robotPositionY]);
        statesPossibles.push([robotPositionX--, robotPositionY]);
        statesPossibles.push([robotPositionX, robotPositionY++]);
        statesPossibles.push([robotPositionX, robotPositionY--]);

        const thirdArray = statesPossibles.filter((elem) => {
          return robot_states.some((ele) => {
            return ele[0] === elem[0] && ele[1] === elem[1];
          });
        });

        if (thirdArray.length === statesPossibles.length) {
          return true;
        }

        if (
          robotPositionX > room_size - 1 ||
          robotPositionX < 0 ||
          robotPositionY > room_size - 1 ||
          robotPositionY < 0 ||
          hasState
        ) {
          return false;
        }

        return true;
      };

      // Decide how direction to go
      const randomMovement = Math.floor(Math.random() * 4);
      switch (randomMovement) {
        case 0:
          // Move UP
          console.log("Moving to UP");
          robotPositionX--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 1:
          // Move DOWN
          console.log("Moving to DOWN");
          robotPositionX++;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 2:
          // Move RIGHT
          console.log("Moving to RIGHT");
          robotPositionY++;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 3:
          // Move LEFT
          console.log("Moving to LEFT");
          robotPositionY--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;

        default:
          // Move UP
          console.log("Moving to UP");
          robotPositionX--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
      }

      // Cleaner action
      if (findOtherRoom) {
        console.log("===========================================");
        console.log("Wall finded! Calculating other route...");
        console.log("===========================================");

        robotPositionX = initialRobotPositionX;
        robotPositionY = initialRobotPositionY;
      } else {
        const currentRoom = spaces.get([robotPositionX, robotPositionY]);

        console.log(
          spaces.get([robotPositionX, robotPositionY]).get_room_position()
        );

        if (currentRoom.is_clean()) {
          console.log("Space already clean");
          lose_points();
        } else {
          console.log("Cleaning...");
          currentRoom.clean_state();
          win_points();
        }

        const hasState = robot_states.some(
          (states) =>
            states &&
            states[0] === initialRobotPositionX &&
            states[1] === initialRobotPositionY
        );

        if (!hasState) {
          robot_states.push([initialRobotPositionX, initialRobotPositionY]);
        }
      }
    }
  }

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
