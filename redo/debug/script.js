function setup() {
  createCanvas(400, 400);
  let img = createImage(28, 28);
  img.loadPixels();
  console.log("pixels: " + img.pixels);
  console.log("length: " + img.pixels.length);
  console.log("width * heigt * 4: " + img.width * img.height * 4);
  img.updatePixels();
}
