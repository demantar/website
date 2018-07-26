function setup() {
  createCanvas(400, 400);
  loadPixels();
  console.log("pixels: " + pixels);
  console.log("length: " + pixels.length);
  console.log("width * heigt * 4: " + width * height * 4);
  updatePixels();
}
