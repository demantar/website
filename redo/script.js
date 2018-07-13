
// let model;
// let canvas;
// let data;
// let pdata;
// let predbutton;
// let clearbutton;
//
// async function main() {
//   let ROOT_URL = location.href;
//   ROOT_URL = ROOT_URL.substring(0, ROOT_URL.length - 10);
//   console.log(ROOT_URL);
//   const MODEL_URL = ROOT_URL + 'jsmodel/tensorflowjs_model.pb';
//   const WEIGHTS_URL = ROOT_URL + 'jsmodel/weights_manifest.json';
//
//   console.log(ROOT_URL);
//   console.log(MODEL_URL);
//   console.log(WEIGHTS_URL);
//
//   console.log("loading");
//   model = await tf.loadFrozenModel(MODEL_URL, WEIGHTS_URL);
//   console.log("loading finneshed");
//
//   predbutton = createButton('predict');
//   predbutton.mousePressed(logPrediction);
// }
//
// async function getPrediction() {
//   loadPixels();
//   pdata = [];
//   console.log("pixels:");
//   console.log(pixels);
//   for (let i = 0; i < pixels.length; i += 4) {
//     console.log(pixels[i]);
//     pdata[i / 4] = pixels[i] / 255
//   }
//   console.log(pdata);
//   return model.execute({
//     input: tf.tensor(pdata, [1, 784]),
//     keep_probability: tf.tensor(1)
//   });
// }
//
// async function logPrediction() {
//   let pred = await getPrediction();
//   pred = tf.softmax(pred);
//   let predData = await pred.data();
//   console.log(predData);
// }
//
// function clear() {
//   background(0);
// }
//
// function setup() {
//   createCanvas(28, 28);
//   background(0);
//   // clear();
//   stroke(255);
//   // clearbutton = createButton('clear');
//   // clearbutton.mousePressed(clear);
//   main();
// }
//
// function mouseDragged() {
//   point(mouseX, mouseY);
// }






var s = function (sk) {
  sk.setup = function() {
    sk.createCanvas(28, 28);
    sk.background(0);
    sk.stroke(255)
  }

  sk.mouseDragged = function() {
    sk.line(mouseX, mouseY, pmouseX, pmouseY);
  }
}

sketch = new p5(s);
