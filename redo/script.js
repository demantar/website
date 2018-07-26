
let model;
let data;
let pdata;
let predbutton;

async function printPixels(sk) {
  sk.loadPixels();
  console.log("pixels");
  console.log(sk.pixels);
  sk.pixels = sk.pixels;
  sk.updatePixels();
}

async function main(sk) {
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

  predbutton = sk.createButton('predict');
  predbutton.mousePressed(() => logPrediction(sk));
}

async function logPrediction(sk) {
  let pred = await getPrediction(sk);
  pred = tf.softmax(pred);
  let predData = await pred.data();
  console.log(predData);
}

async function getPrediction(sk) {
  sk.loadPixels();
  pdata = [];
  console.log("pixels:");
  console.log(sk.pixels);
  for (let x = 0; x < sk.width; x++) {
    for (let y = 0; y < sk.height; y++) {
      let i = x + y * sk.width * 4;
      //console.log(sk.pixels[i]);
      pdata.push(sk.pixels[i] / 255);
    }
  }
  sk.updatePixels();
  console.log(pdata);
  return model.execute({
    input: tf.tensor(pdata, [1, 784]),
    keep_probability: tf.tensor(1)
  });
}

var s = function (sk) {
  sk.setup = function() {
    sk.createCanvas(28, 28);
    sk.background(0);
    sk.stroke(255);
    sk.pixelDensity(1);
    main(sk);
  }

  sk.mouseDragged = function() {
    sk.line(sk.mouseX, sk.mouseY, sk.pmouseX, sk.pmouseY);
  }

  sk.mouseReleased = function() {
    printPixels(sk);
  }
}


sketch = new p5(s);
