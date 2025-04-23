const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Store confiscated tech (simple in-memory object: { alien_id: tech_description })
const confiscated_tech = {};
let tech_counter = 0; // Simple way to generate unique IDs

// Simulate random failure (e.g., weapon unexpectedly discharges)
function simulateFailure(probability = 0.2) {
  // Reduced probability slightly
  return Math.random() < probability;
}

app.post("/confiscate", (req, res) => {
  const alien_id = req.body.alien_id;
  if (!alien_id) {
    return res.status(400).json({ message: "Missing alien_id" });
  }

  console.log(`Attempting tech confiscation for alien: ${alien_id}`);

  if (simulateFailure()) {
    console.error(
      `Tech confiscation failed for alien: ${alien_id} (e.g., plasma leak)`
    );
    return res
      .status(500)
      .json({ message: `Error confiscating tech from ${alien_id}` });
  }

  const tech_id = `plasma_weapon_${tech_counter++}`;
  confiscated_tech[alien_id] = tech_id; // Store alien_id -> tech_id mapping
  console.log(`Tech ${tech_id} confiscated from alien ${alien_id}`);
  res
    .status(200)
    .json({
      message: `Technology confiscated from ${alien_id}`,
      tech_id: tech_id,
    });
});

app.post("/return-tech", (req, res) => {
  const alien_id = req.body.alien_id;
  if (!alien_id) {
    return res.status(400).json({ message: "Missing alien_id" });
  }

  const tech_id = confiscated_tech[alien_id];

  if (tech_id) {
    delete confiscated_tech[alien_id]; // Remove the entry
    console.log(`Compensation: Tech ${tech_id} returned to alien ${alien_id}`);
    res
      .status(200)
      .json({ message: `Confiscated tech ${tech_id} returned to ${alien_id}` });
  } else {
    console.warn(
      `Compensation: No confiscated tech found for alien ${alien_id}`
    );
    res
      .status(404)
      .json({ message: `No confiscated tech record found for ${alien_id}` });
  }
});

app.get("/confiscated-items", (req, res) => {
  res.status(200).json(confiscated_tech);
});

app.listen(5002, () => {
  // Keep port or change if needed
  console.log("Tech Confiscation Service listening on port 5002");
});
