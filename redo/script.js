
let model;
let canvas;

async function main() {
  let ROOT_URL = location.href;
  ROOT_URL = ROOT_URL.substring(0, ROOT_URL.length - 10);
  console.log(ROOT_URL);
  const MODEL_URL = ROOT_URL + 'jsmodel/tensorflowjs_model.pb';
  const WEIGHTS_URL = ROOT_URL + 'jsmodel/weights_manifest.json';

  console.log(ROOT_URL);
  console.log(MODEL_URL);
  console.log(WEIGHTS_URL);

  model = await tf.loadFrozenModel(MODEL_URL, WEIGHTS_URL);
}

function setup() {
  canvas = createCanvas(28, 28);
  canvas = canvas.elt.getContext("2d");
  background(0);
}

main();

function draw() {
  if (model != null) {
    data = canvas.getIgamgeData(0, 0, 28, 28);
    pdata = [];
    for (let i = 0; i < data.length; i += 4) {
      pdata = 255 - data[i]
    }
    console.log(pdata);
  }

  if (mouseIsPressed) {
    point(mouseX, mouseY);
  }
}
