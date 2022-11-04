const { exec } = require("child_process");
const express = require("express");
const app = express();
const open = require("open");

const fs = require("fs");

const bodyParser = require("body-parser");

app.set("view engine", "pug");
app.use(express.static("./public"));

app.use(bodyParser.urlencoded({ extended: false }));

app.use(bodyParser.json());

app.post("/generate", (req, res) => {
  const src = req.body.src;

  fs.mkdirSync("./coconut/result", { recursive: true });
  fs.rmdirSync("./coconut/result", { recursive: true });
  fs.mkdirSync("./coconut/result", { recursive: true });

  var child = exec(`python main.py ${src}`);
  child.stdout.pipe(process.stdout);
  child.on("exit", function () {
    fs.readdir("./coconut/result", (err, files) => {
      if (err) return res.json({ err: `Failed Loading File DIR` });
      if (files.length === 0) return res.json({ err: `Failed` });
      const name = new Date()
        .toISOString()
        .replace(/T/, " ")
        .replace(/\..+/, "")
        .replace(/:/gm, "-");

      fs.rename(
        `./coconut/result/${files[files.length - 1]}`,
        `./public/pdf/${name}.pdf`,
        (err) => {
          if (err) return res.json({ err: `Failed Loading File MOVE` });
          res.json({ res: `/pdf/${name}.pdf` });
        }
      );
    });
  });
});

app.get("/", (req, res, next) => {
  res.render("index.pug");
});

app.use((req, res) => {
  res.status(404).send("Not Found!");
});

app.listen(3000, (err) => {
  if (err) throw err;
  console.log("Application is online!");
  open(`http://localhost:3000`);
});
