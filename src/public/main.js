const bt = document.querySelector(".m-process-bt");
const input = document.querySelector(".m-input");
const loading = document.querySelector(".m-loading");

let busy = false;
bt.onclick = () => {
  if (busy) return;
  busy = true;

  bt.innerHTML = "LOADING";
  bt.style.backgroundColor = "#1c396e";
  loading.style.opacity = 1;

  fetch("/generate", {
    method: "POST",
    body: JSON.stringify({ src: input.value }),
    json: true,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  })
    .then(async (response) => {
      const data = await response.json();
      if (data.err) {
        alert("ERROR Check Console");
        console.log(data.err);
      } else {
        window.open(data.res, "_blank");
      }
      
      bt.removeAttribute("style");
      loading.removeAttribute("style");
      bt.innerHTML = "START";
      busy = false;
    })
    .catch((err) => {
      bt.removeAttribute("style");
      loading.removeAttribute("style");
      bt.innerHTML = "START";
      busy = false;
    });
};

const PRJsCOLOR = "#ffffff";
particlesJS("particles-js", {
  particles: {
    number: { value: 70, density: { enable: true, value_area: 1000 } },
    color: { value: PRJsCOLOR },
    shape: {
      type: "circle",
      stroke: { width: 0, color: PRJsCOLOR },
      polygon: { nb_sides: 5 },
    },
    opacity: {
      value: 0.5,
      random: false,
      anim: { enable: false, speed: 1, opacity_min: 0.5, sync: false },
    },
    size: {
      value: 2,
      random: true,
      anim: { enable: false, speed: 40, size_min: 0.1, sync: false },
    },
    line_linked: {
      enable: true,
      distance: 150,
      color: PRJsCOLOR,
      opacity: 0.4,
      width: 1,
    },
    move: {
      enable: true,
      speed: 6,
      direction: "none",
      random: true,
      straight: false,
      out_mode: "out",
      bounce: false,
      attract: { enable: false, rotateX: 4329.212564336912, rotateY: 1200 },
    },
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: { enable: false, mode: "repulse" },
      onclick: { enable: false, mode: "repulse" },
      resize: true,
    },
    modes: {
      grab: { distance: 400, line_linked: { opacity: 1 } },
      bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
      repulse: { distance: 200, duration: 0.4 },
      push: { particles_nb: 4 },
      remove: { particles_nb: 2 },
    },
  },
  retina_detect: true,
});
