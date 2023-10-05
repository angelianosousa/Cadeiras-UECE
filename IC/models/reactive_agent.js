module.exports = class ReactiveAgent {

  constructor(){
    this.points = 0;
  }

  start_clean(spaces){
    spaces.forEach(function (space, index) {
      if (space.is_clean()){
        console.log(`Room ${index} clean`);
        console.log('>>> Turning to right');
        console.log('=======================>')
        // this.points -= 1;
      } else {
        console.log(`Cleaning room ${index}...`);
        space.clean_state();
        console.log('Turning to left');
        console.log('=======================>')
        // this.points += 1;
      }
    });
  }

  show_points(){
    return this.points
  }

}
