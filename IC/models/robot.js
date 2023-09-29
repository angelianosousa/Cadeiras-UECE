module.exports = class Robot {

  constructor(){
    this.space_counting = 0;
  }

  start(spaces){
    spaces.forEach(function (space) {
      // let robot = new Robot();
      // this.clean(space);
      if (space.is_clean()){
        console.log('Space clean');
      } else {
        console.log('Cleaning...');
        space.clean_state();
        // this.set_space_counting();
      }
    });
  }

  set_space_counting(){
    this.space_counting += 1;
  }

  // clean(space){
    
  // }
}