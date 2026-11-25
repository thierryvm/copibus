// iPhone bench for Copibus phase 0 (chantier E).
// Each test records a short result. The report never contains an exact position:
// only accuracy, counts, durations and yes/no answers.
"use strict";

const results = {};
const standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
document.getElementById("mode").textContent = standalone
  ? "Mode : app installée (écran d'accueil)"
  : "Mode : Safari. Installe la page sur l'écran d'accueil pour le test complet.";

function setResult(id, ok, text) {
  results[id] = { ok, text, at: new Date().toLocaleTimeString("fr-BE") };
  const el = document.getElementById("st-" + id);
  el.textContent = ok === null ? text : (ok ? "OK" : "Échec");
  el.className = "st " + (ok === null ? "" : ok ? "ok" : "ko");
  document.getElementById("out-" + id).textContent = text;
  renderReport();
}

const TESTS = [
  { id: "gps", title: "1. GPS", help: "Suit la position 30 min, écran allumé. Rien n'est enregistré sauf la précision.",
    buttons: [["Démarrer", startGps], ["Arrêter", stopGps, true]] },
  { id: "wake", title: "2. Écran allumé", help: "Garde l'écran allumé. Va sur une autre app puis reviens : le verrou doit revenir seul.",
    buttons: [["Activer", startWake]] },
  { id: "voice", title: "3. Voix française", help: "Liste les voix françaises et lit une phrase. Vérifie si la bouche peut suivre les mots.",
    buttons: [["Lire une phrase", speak]] },
  { id: "sound", title: "4. Son", help: "Joue un bip. Refais-le avec le bouton silence activé, puis avec le Bluetooth.",
    buttons: [["Jouer un bip", beep]] },
  { id: "storage", title: "5. Carte hors ligne", help: "Écrit 14 Mo dans le stockage de l'app (taille de la carte du corridor), puis les relit. Refais « Relire » en mode avion.",
    buttons: [["Écrire 14 Mo", writeStorage], ["Relire", readStorage, true]] },
];

const root = document.getElementById("tests");
for (const t of TESTS) {
  const card = document.createElement("div");
  card.className = "t";
  card.innerHTML = `<h2><span>${t.title}</span><span class="st" id="st-${t.id}">—</span></h2><p>${t.help}</p>`;
  for (const [label, fn, sec] of t.buttons) {
    const b = document.createElement("button");
    b.textContent = label;
    if (sec) b.className = "sec";
    b.addEventListener("click", () => fn().catch((e) => setResult(t.id, false, String(e && e.message || e))));
    card.appendChild(b);
  }
  const pre = document.createElement("pre");
  pre.id = "out-" + t.id;
  card.appendChild(pre);
  root.appendChild(card);
}

// --- 1. GPS -----------------------------------------------------------------
let gpsWatch = null, gps = null;
async function startGps() {
  if (!("geolocation" in navigator)) return setResult("gps", false, "Pas de géolocalisation.");
  if (gpsWatch !== null) return;
  gps = { start: Date.now(), fixes: 0, best: Infinity, worst: 0, sumAcc: 0, maxGap: 0, last: Date.now(), errors: 0 };
  gpsWatch = navigator.geolocation.watchPosition((p) => {
    const now = Date.now();
    gps.maxGap = Math.max(gps.maxGap, now - gps.last);
    gps.last = now;
    gps.fixes++;
    const a = p.coords.accuracy;
    gps.best = Math.min(gps.best, a); gps.worst = Math.max(gps.worst, a); gps.sumAcc += a;
    showGps(null);
  }, (e) => { gps.errors++; showGps(false, e.message); }, { enableHighAccuracy: true, maximumAge: 0, timeout: 20000 });
  showGps(null);
}
function showGps(ok, err) {
  const min = ((Date.now() - gps.start) / 60000).toFixed(1);
  const avg = gps.fixes ? Math.round(gps.sumAcc / gps.fixes) : "-";
  const text = `durée ${min} min, ${gps.fixes} positions, précision moy. ${avg} m (meilleure ${Math.round(gps.best)} m, pire ${Math.round(gps.worst)} m), plus long trou ${Math.round(gps.maxGap / 1000)} s, erreurs ${gps.errors}${err ? " (" + err + ")" : ""}`;
  setResult("gps", ok === null ? (gps.fixes > 0 ? null : null) : ok, text);
}
async function stopGps() {
  if (gpsWatch === null) return;
  navigator.geolocation.clearWatch(gpsWatch);
  gpsWatch = null;
  const min = (Date.now() - gps.start) / 60000;
  showGps(gps.fixes > 0 && gps.maxGap < 30000 && min >= 1);
}

// --- 2. Wake Lock --------------------------------------------------------------
let wakeLock = null, wakeWanted = false, wakeReacquired = 0, wakeReleased = 0;
async function acquireWake() {
  wakeLock = await navigator.wakeLock.request("screen");
  wakeLock.addEventListener("release", () => { wakeReleased++; showWake(); });
}
async function startWake() {
  if (!("wakeLock" in navigator)) return setResult("wake", false, "Wake Lock absent.");
  wakeWanted = true;
  await acquireWake();
  showWake();
}
function showWake() {
  const active = wakeLock && !wakeLock.released;
  setResult("wake", active, `verrou ${active ? "actif" : "relâché"}, relâché ${wakeReleased} fois, repris ${wakeReacquired} fois`);
}
document.addEventListener("visibilitychange", async () => {
  if (document.visibilityState === "visible" && wakeWanted && (!wakeLock || wakeLock.released)) {
    try { await acquireWake(); wakeReacquired++; } catch (e) { /* reported below */ }
    showWake();
  }
});

// --- 3. Voices and boundary events -------------------------------------------
function frVoices() {
  return speechSynthesis.getVoices().filter((v) => v.lang.toLowerCase().startsWith("fr"));
}
async function speak() {
  if (!("speechSynthesis" in window)) return setResult("voice", false, "Synthèse vocale absente.");
  let voices = frVoices();
  if (!voices.length) {
    await new Promise((r) => { speechSynthesis.onvoiceschanged = r; setTimeout(r, 1500); });
    voices = frVoices();
  }
  const u = new SpeechSynthesisUtterance("Prochain arrêt : Guillemins, quai D. Départ dans trois minutes.");
  u.lang = "fr-BE";
  const be = voices.find((v) => v.lang === "fr-BE");
  u.voice = be || voices[0] || null;
  let boundaries = 0;
  const t0 = performance.now();
  u.onboundary = () => { boundaries++; };
  await new Promise((resolve) => {
    u.onend = resolve; u.onerror = (e) => { boundaries = -1; resolve(e); };
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  });
  const ms = Math.round(performance.now() - t0);
  const names = voices.map((v) => `${v.name} (${v.lang})`).join(", ") || "aucune";
  setResult("voice", voices.length > 0 && boundaries > 0,
    `${voices.length} voix FR : ${names}. Voix utilisée : ${u.voice ? u.voice.name : "défaut"}. Événements « mot » : ${boundaries}. Durée ${ms} ms.`);
}

// --- 4. Sound unlock -------------------------------------------------------------
let audioCtx = null, beeps = 0;
async function beep() {
  audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
  if (audioCtx.state !== "running") await audioCtx.resume();
  const o = audioCtx.createOscillator(), g = audioCtx.createGain();
  o.frequency.value = 880; g.gain.value = 0.3;
  o.connect(g).connect(audioCtx.destination);
  o.start(); o.stop(audioCtx.currentTime + 0.4);
  beeps++;
  setResult("sound", audioCtx.state === "running",
    `contexte audio ${audioCtx.state}, ${beeps} bip(s). Note à la main si tu l'as entendu (silence, Bluetooth).`);
}

// --- 5. OPFS storage ----------------------------------------------------------------
const SIZE = 14 * 1024 * 1024;
async function opfsFile(create) {
  const dir = await navigator.storage.getDirectory();
  return dir.getFileHandle("corridor-test.bin", { create });
}
async function writeStorage() {
  if (!navigator.storage || !navigator.storage.getDirectory) return setResult("storage", false, "OPFS absent.");
  const persisted = navigator.storage.persist ? await navigator.storage.persist() : false;
  const data = new Uint8Array(SIZE);
  for (let i = 0; i < SIZE; i += 4096) data[i] = i % 251;
  const t0 = performance.now();
  const h = await opfsFile(true);
  const w = await h.createWritable();
  await w.write(data); await w.close();
  const ms = Math.round(performance.now() - t0);
  const est = navigator.storage.estimate ? await navigator.storage.estimate() : {};
  const quota = est.quota ? Math.round(est.quota / 1048576) + " Mo" : "inconnu";
  setResult("storage", true, `14 Mo écrits en ${ms} ms. Stockage persistant : ${persisted ? "oui" : "non"}. Quota : ${quota}.`);
}
async function readStorage() {
  const t0 = performance.now();
  const f = await (await opfsFile(false)).getFile();
  const buf = new Uint8Array(await f.arrayBuffer());
  let ok = buf.length === SIZE;
  for (let i = 0; ok && i < SIZE; i += 4096) ok = buf[i] === i % 251;
  const ms = Math.round(performance.now() - t0);
  setResult("storage", ok, `relu ${Math.round(f.size / 1048576)} Mo en ${ms} ms, contenu ${ok ? "intact" : "abîmé"}, en ligne : ${navigator.onLine ? "oui" : "non"}.`);
}

// --- Report --------------------------------------------------------------------------
function renderReport() {
  const lines = [
    "Rapport banc iPhone (Copibus)",
    `date ${new Date().toLocaleString("fr-BE")}`,
    `mode ${standalone ? "installée" : "Safari"}, en ligne ${navigator.onLine ? "oui" : "non"}`,
    `appareil ${navigator.userAgent.match(/OS [\d_]+/)?.[0]?.replace(/_/g, ".") || navigator.platform}`,
  ];
  for (const t of TESTS) {
    const r = results[t.id];
    lines.push(`${t.title} : ${r ? (r.ok === null ? "en cours" : r.ok ? "OK" : "ÉCHEC") + " (" + r.at + ") " + r.text : "pas fait"}`);
  }
  document.getElementById("report").textContent = lines.join("\n");
}
document.getElementById("copy").addEventListener("click", async () => {
  renderReport();
  try { await navigator.clipboard.writeText(document.getElementById("report").textContent); alert("Rapport copié."); }
  catch { alert("Copie impossible : fais un appui long sur le texte."); }
});
renderReport();

if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
