function setup() {
  createCanvas(28, 28);
  loadPixels();
  console.log("pixels: " + pixels);
  console.log("length: " + pixles.length);
  console.log("width * heigt * 4: " + width * height * 4);
  updatePixels();
}
