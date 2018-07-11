
let model;
let canvas;
let data;
let pdata;
let predbutton;
let clearbutton;

async function main() {
  let ROOT_URL = location.href;
  ROOT_URL = ROOT_URL.substring(0, ROOT_URL.length - 10);
  console.log(ROOT_URL);
  const MODEL_URL = ROOT_URL + 'jsmodel/tensorflowjs_model.pb';
  const WEIGHTS_URL = ROOT_URL + 'jsmodel/weights_manifest.json';

  console.log(ROOT_URL);
  console.log(MODEL_URL);
  console.log(WEIGHTS_URL);

  console.log("loading");
  model = await tf.loadFrozenModel(MODEL_URL, WEIGHTS_URL);
  console.log("loading finneshed");

  predbutton = createButton('predict');
  predbutton.mousePressed(logPrediction);
}

async function getPrediction() {
  data = canvas.getImageData(0, 0, 28, 28).data;
  pdata = [];
  for (let i = 0; i < data.length; i += 4) {
    pdata[i / 4] = data[i] / 255
  }
  console.log(pdata);
  return model.execute({
    input: tf.tensor(pdata, [1, 784]),
    keep_probability: tf.tensor(1)
  });
}

async function logPrediction() {
  let pred = await getPrediction();
  pred = tf.softmax(pred);
  let predData = await pred.data();
  console.log(predData);
}

function clear() {
  background(0);
}

function setup() {
  canvas = createCanvas(28, 28);
  canvas = canvas.elt.getContext("2d");
  background(0);
  // clear();
  stroke(255);
  // clearbutton = createButton('clear');
  // clearbutton.mousePressed(clear);
}

function mousePressed() {
  point(mouseX, mouseY);
}

main();
