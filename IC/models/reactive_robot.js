const Math = require("mathjs");

module.exports = class ReactiveRobot {
  constructor() {
    this.space_counting = 0;
  }

  win_points() {
    this.space_counting += 1;
  }

  lose_points() {
    this.space_counting -= 1;
  }

  async start_reactive_bot(spaces) {
    const win_points        = () => this.win_points();
    const lose_points       = () => this.lose_points();
    const get_points        = () => this.space_counting;

    /**
     * [0,0][0,1][0,2]
     * [1,0][1,1][1,2]
     * [2,0][2,1][2,2]
     */

    let start          = true;
    let room_size      = spaces._data.length;
    let robotPositionX = 0;
    let robotPositionY = 0;

    while (start) {
      // Check if room was cleaned
      spaces.forEach(function (space) {
        if (space.is_spaces_clear() && start) {
          console.log("All Cleaned!!");

          console.log("Total points: ", get_points());
          console.log('=======================================================');
          
          start = false;
        }
      });
      
      if (!start) break;

      // Await for a second
      await new Promise((r) => setTimeout(r, 1000));

      // Variables
      let findOtherRoom = false;

      let rooms_state = [];

      let initialRobotPositionX = robotPositionX;
      let initialRobotPositionY = robotPositionY;

      // Print room
      for (let line = 0; line < room_size; line++) {
        rooms_state[line] = [];
        for (let column = 0; column < room_size; column++) {
          rooms_state[line][column] = spaces.get([line, column]).state_room;
        }
      }

      console.table(rooms_state);

      const verifyIfRoomIsAble = () => {
        if (
          robotPositionX > room_size - 1 ||
          robotPositionX < 0             ||
          robotPositionY > room_size - 1 ||
          robotPositionY < 0
        ) {
          return false;
        }

        return true;
      };

      // Decide what direction to go
      const randomMovement = Math.floor(Math.random() * 4);
      switch (randomMovement) {
        case 0:
          console.log("Moving UP");
          robotPositionX--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 1:
          console.log("Moving DOWN");
          robotPositionX++;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 2:
          console.log("Moving RIGHT");
          robotPositionY++;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
        case 3:
          console.log("Moving LEFT");
          robotPositionY--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;

        default:
          console.log("Moving to UP");
          robotPositionX--;

          if (!verifyIfRoomIsAble()) findOtherRoom = true;
          break;
      }

      // Cleaner action
      if (findOtherRoom) {
        console.log("=======================================================");
        console.log("Wall finded! Calculating other route...");
        console.log("=======================================================");

        robotPositionX = initialRobotPositionX;
        robotPositionY = initialRobotPositionY;
      } else {
        const currentRoom = spaces.get([robotPositionX, robotPositionY]);

        if (currentRoom.is_clean()) {
          console.log("=======================================================");
          console.log("Space", currentRoom.position, 'already clean!');
          lose_points();
        } else {
          console.log("Cleaning...", currentRoom.position);
          console.log("=======================================================");
          currentRoom.clean_state();
          win_points();
        }
      }
    }
  }
}