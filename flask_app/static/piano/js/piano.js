// JSON object containing all relevant sound information for piano
const sound = {
  65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
  87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
  83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
  69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  59: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// Creepy audio link
const creepyAudio = new Audio("https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1");

// Boolean to check for playability of piano
let playable = true;

// String to check for alien appearance condition
let str = "";

// Array of black keys for color change purposes
const blacks = ['W','E','T','Y','U','O','P'];

// Elements pulled from html
const pianoElem = document.getElementsByClassName("piano");
const alienImg = document.getElementsByClassName("amygdala-img");
const notes = document.querySelectorAll(".note");
const keys = document.querySelectorAll(".key");

// Audio playback
let playNote = (e) => {
  const noteSound = new Audio(sound[e]);
  noteSound.currentTime = 0;
  noteSound.play();
};

// Plays creepy audio, hides piano
function hidePiano(element) {
  creepyAudio.play();
  element.style.animation = "fadeOut 2.5s";
  setTimeout(() => {
    element.style.display = "none";
  }, 2400);
  playable = false;
  showAmygdala(alienImg[0]);
}

// Shows alien image
function showAmygdala(element) {
  setTimeout(() => {
    element.style.display = "flex";
  }, 2400);
}

// Checks if sound is playable, and all right conidtions are met
function checkPlayability(iLetter){
  let letter = iLetter.toUpperCase();
  str += letter;
  if (str.substring(str.length - 8) == 'WESEEYOU') {
    hidePiano(pianoElem[0]);
  }
  console.log(letter);
  if (playable) {
    playNote(letter.charCodeAt(0));
  }
}

// Keydown listener
document.addEventListener('keydown', (e) => {
  checkPlayability(e.key);
});

for (let key of keys){
  // Click listener
  key.addEventListener("click", (event) => {
    event.target.style.backgroundColor = '#ccc';
    checkPlayability(event.target.id);
    setTimeout(() => {
      if(blacks.includes(event.target.id.toUpperCase())){
        event.target.style.backgroundColor = 'rgb(94, 83, 83)';
      }
      else{
        event.target.style.backgroundColor = 'white';
      }
    }, 200);
  }); 

  // Mouseover listener
  key.addEventListener("mouseover", (event) => {
    for (let note of notes){
      note.style.opacity = '1';
    }
  });

  // Mouseout listener
  key.addEventListener("mouseout", (event) => {
    for (let note of notes){
      note.style.opacity = '0';
    }
  });
}