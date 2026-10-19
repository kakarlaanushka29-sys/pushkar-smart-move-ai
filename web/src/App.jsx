import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";
const color = { AVAILABLE: "#22c55e", FILLING: "#eab308", FULL_RISK: "#ef4444" };
const dcolor = { LOW: "#22c55e", MEDIUM: "#eab308", HIGH: "#ef4444" };
const tcolor = { LOW: "#22c55e", MODERATE: "#eab308", HIGH: "#ef4444" };
const LEVELS = ["LOW", "MODERATE", "HIGH"];
const STATUSES = ["Reported", "Acknowledged", "Team Assigned", "Help Arrived", "Resolved"];
const CATEGORIES = ["Accident", "Injured pilgrim", "Medical emergency", "Missing person", "Crowd emergency", "Other"];
const LOCATIONS = ["Ghat A", "Ghat B", "Entry Gate C", "Parking A", "Parking B"];
const SHUTTLE_STATUSES = ["Running", "Delayed", "Disrupted"];

// NOTE: Telugu/Hindi texts are DRAFT. Get native speakers to verify before real use.
const T = {
  en: {
    title: "Pushkar Smart Move AI", pilgrim: "Pilgrim View", sos: "SOS", admin: "Admin View",
    traffic: "Traffic (simulated data)", closed: "CLOSED", min: "min", trafficWord: "traffic",
    recRoute: "Recommended route", parkingStatus: "Parking Status", parking: "Parking", ghat: "Ghat",
    available: "Available", full: "full", recommended: "Recommended", spacesFree: "spaces free",
    allFull: "All parking nearly full", shuttles: "Shuttles to Ghat", status: "Status",
    every: "Every", running: "shuttle(s) running", waiting: "Waiting", demand: "Demand",
    emergencyHelp: "Emergency Help", call112: "Life-threatening emergency? Call 112 immediately.",
    emergencyType: "Emergency type", location: "Location", useGps: "Use my GPS (optional)",
    gpsOk: "GPS location captured", gpsDenied: "GPS denied. Please select location manually.",
    gpsNA: "GPS not supported. Select location manually.", sendSos: "SEND SOS",
    notSent: "Report NOT sent. Call 112 now!", report: "Report", sent: "sent",
    incidents: "Emergency Incidents", noIncidents: "No incidents.",
    adminTraffic: "Admin: Traffic (simulated)", adminShuttles: "Admin: Shuttles (simulated data)",
    adminParking: "Admin: Update Parking", assign: "+ Assign", remove: "- Remove",
    runningShuttles: "Running shuttles", addMore: "Suggest adding {n} more shuttle(s). Admin to confirm.",
    enough: "Enough shuttles for current demand.", disrupted: "Route disrupted. Use another route.",
    parkStatus: { AVAILABLE: "AVAILABLE", FILLING: "FILLING", FULL_RISK: "NEARLY FULL" },
    level: { LOW: "LOW", MODERATE: "MODERATE", HIGH: "HIGH" },
    demandL: { LOW: "LOW", MEDIUM: "MEDIUM", HIGH: "HIGH" },
    sosStatus: { Reported: "Reported", Acknowledged: "Acknowledged", "Team Assigned": "Team Assigned", "Help Arrived": "Help Arrived", Resolved: "Resolved" },
    shStatus: { Running: "Running", Delayed: "Delayed", Disrupted: "Disrupted" },
    cat: { Accident: "Accident", "Injured pilgrim": "Injured pilgrim", "Medical emergency": "Medical emergency", "Missing person": "Missing person", "Crowd emergency": "Crowd emergency", Other: "Other" },
    loc: { "Ghat A": "Ghat A", "Ghat B": "Ghat B", "Entry Gate C": "Entry Gate C", "Parking A": "Parking A", "Parking B": "Parking B" },
    roads: { 1: "Main Road to Ghat A", 2: "Bypass Road via Parking B", 3: "Riverside Road" },
  },
  te: {
    title: "పుష్కర్ స్మార్ట్ మూవ్ AI", pilgrim: "యాత్రికుల వీక్షణ", sos: "SOS", admin: "అడ్మిన్ వీక్షణ",
    traffic: "ట్రాఫిక్ (సిమ్యులేటెడ్ డేటా)", closed: "మూసివేయబడింది", min: "నిమిషాలు", trafficWord: "ట్రాఫిక్",
    recRoute: "సిఫార్సు చేసిన మార్గం", parkingStatus: "పార్కింగ్ స్థితి", parking: "పార్కింగ్", ghat: "ఘాట్",
    available: "ఖాళీ", full: "నిండింది", recommended: "సిఫార్సు", spacesFree: "ఖాళీ స్థలాలు",
    allFull: "అన్ని పార్కింగ్‌లు దాదాపు నిండిపోయాయి", shuttles: "ఘాట్‌కు షటిల్స్", status: "స్థితి",
    every: "ప్రతి", running: "షటిల్(లు) నడుస్తున్నాయి", waiting: "వేచి ఉన్నవారు", demand: "డిమాండ్",
    emergencyHelp: "అత్యవసర సహాయం", call112: "ప్రాణాపాయ పరిస్థితా? వెంటనే 112 కు కాల్ చేయండి.",
    emergencyType: "అత్యవసర రకం", location: "ప్రదేశం", useGps: "నా GPS వాడండి (ఐచ్ఛికం)",
    gpsOk: "GPS స్థానం నమోదైంది", gpsDenied: "GPS అనుమతి లేదు. దయచేసి ప్రదేశాన్ని ఎంచుకోండి.",
    gpsNA: "GPS అందుబాటులో లేదు. ప్రదేశాన్ని ఎంచుకోండి.", sendSos: "SOS పంపండి",
    notSent: "రిపోర్ట్ పంపబడలేదు. వెంటనే 112 కు కాల్ చేయండి!", report: "రిపోర్ట్", sent: "పంపబడింది",
    incidents: "అత్యవసర సంఘటనలు", noIncidents: "సంఘటనలు లేవు.",
    adminTraffic: "అడ్మిన్: ట్రాఫిక్ (సిమ్యులేటెడ్)", adminShuttles: "అడ్మిన్: షటిల్స్ (సిమ్యులేటెడ్ డేటా)",
    adminParking: "అడ్మిన్: పార్కింగ్ అప్డేట్", assign: "+ కేటాయించు", remove: "- తొలగించు",
    runningShuttles: "నడుస్తున్న షటిల్స్", addMore: "మరో {n} షటిల్(లు) జోడించమని సూచన. అడ్మిన్ నిర్ధారించాలి.",
    enough: "ప్రస్తుత డిమాండ్‌కు షటిల్స్ సరిపోతాయి.", disrupted: "మార్గం అంతరాయం. మరో మార్గం వాడండి.",
    parkStatus: { AVAILABLE: "అందుబాటులో", FILLING: "నిండుతోంది", FULL_RISK: "దాదాపు నిండింది" },
    level: { LOW: "తక్కువ", MODERATE: "మధ్యస్థం", HIGH: "ఎక్కువ" },
    demandL: { LOW: "తక్కువ", MEDIUM: "మధ్యస్థం", HIGH: "ఎక్కువ" },
    sosStatus: { Reported: "నివేదించబడింది", Acknowledged: "గుర్తించబడింది", "Team Assigned": "బృందం కేటాయించబడింది", "Help Arrived": "సహాయం చేరుకుంది", Resolved: "పరిష్కరించబడింది" },
    shStatus: { Running: "నడుస్తోంది", Delayed: "ఆలస్యం", Disrupted: "అంతరాయం" },
    cat: { Accident: "ప్రమాదం", "Injured pilgrim": "గాయపడిన యాత్రికుడు", "Medical emergency": "వైద్య అత్యవసరం", "Missing person": "తప్పిపోయిన వ్యక్తి", "Crowd emergency": "జన సమూహ అత్యవసరం", Other: "ఇతర" },
    loc: { "Ghat A": "ఘాట్ A", "Ghat B": "ఘాట్ B", "Entry Gate C": "ప్రవేశ ద్వారం C", "Parking A": "పార్కింగ్ A", "Parking B": "పార్కింగ్ B" },
    roads: { 1: "ఘాట్ A కు ప్రధాన రహదారి", 2: "పార్కింగ్ B మీదుగా బైపాస్ రోడ్", 3: "నది ఒడ్డు రహదారి" },
  },
  hi: {
    title: "पुष्कर स्मार्ट मूव AI", pilgrim: "यात्री दृश्य", sos: "SOS", admin: "एडमिन दृश्य",
    traffic: "ट्रैफिक (सिमुलेटेड डेटा)", closed: "बंद", min: "मिनट", trafficWord: "ट्रैफिक",
    recRoute: "सुझाया गया मार्ग", parkingStatus: "पार्किंग स्थिति", parking: "पार्किंग", ghat: "घाट",
    available: "उपलब्ध", full: "भरा", recommended: "सुझाव", spacesFree: "स्थान खाली",
    allFull: "सभी पार्किंग लगभग भर चुकी हैं", shuttles: "घाट के लिए शटल", status: "स्थिति",
    every: "हर", running: "शटल चल रही हैं", waiting: "प्रतीक्षा में", demand: "मांग",
    emergencyHelp: "आपातकालीन सहायता", call112: "जानलेवा आपातकाल? तुरंत 112 पर कॉल करें।",
    emergencyType: "आपातकाल का प्रकार", location: "स्थान", useGps: "मेरा GPS उपयोग करें (वैकल्पिक)",
    gpsOk: "GPS स्थान प्राप्त हुआ", gpsDenied: "GPS अनुमति नहीं मिली। कृपया स्थान चुनें।",
    gpsNA: "GPS उपलब्ध नहीं है। स्थान चुनें।", sendSos: "SOS भेजें",
    notSent: "रिपोर्ट नहीं भेजी गई। तुरंत 112 पर कॉल करें!", report: "रिपोर्ट", sent: "भेजी गई",
    incidents: "आपातकालीन घटनाएं", noIncidents: "कोई घटना नहीं।",
    adminTraffic: "एडमिन: ट्रैफिक (सिमुलेटेड)", adminShuttles: "एडमिन: शटल (सिमुलेटेड डेटा)",
    adminParking: "एडमिन: पार्किंग अपडेट", assign: "+ जोड़ें", remove: "- हटाएं",
    runningShuttles: "चल रही शटल", addMore: "{n} और शटल जोड़ने का सुझाव। एडमिन पुष्टि करें।",
    enough: "वर्तमान मांग के लिए शटल पर्याप्त हैं।", disrupted: "मार्ग बाधित। दूसरा मार्ग लें।",
    parkStatus: { AVAILABLE: "उपलब्ध", FILLING: "भर रही है", FULL_RISK: "लगभग भरी" },
    level: { LOW: "कम", MODERATE: "मध्यम", HIGH: "अधिक" },
    demandL: { LOW: "कम", MEDIUM: "मध्यम", HIGH: "अधिक" },
    sosStatus: { Reported: "सूचित", Acknowledged: "स्वीकार किया", "Team Assigned": "टीम नियुक्त", "Help Arrived": "सहायता पहुंची", Resolved: "समाधान हुआ" },
    shStatus: { Running: "चल रही है", Delayed: "देरी", Disrupted: "बाधित" },
    cat: { Accident: "दुर्घटना", "Injured pilgrim": "घायल यात्री", "Medical emergency": "चिकित्सा आपातकाल", "Missing person": "लापता व्यक्ति", "Crowd emergency": "भीड़ आपातकाल", Other: "अन्य" },
    loc: { "Ghat A": "घाट A", "Ghat B": "घाट B", "Entry Gate C": "प्रवेश द्वार C", "Parking A": "पार्किंग A", "Parking B": "पार्किंग B" },
    roads: { 1: "घाट A का मुख्य मार्ग", 2: "पार्किंग B से बाईपास रोड", 3: "नदी किनारे की सड़क" },
  },
};

const put = (url, body) =>
  fetch(`${API}${url}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

const tr = (t, s) => s.replace("Parking", t.parking).replace("Ghat", t.ghat);

function shuttleNote(t, s) {
  if (s.status === "Disrupted") return t.disrupted;
  if (s.extra_needed > 0) return t.addMore.replace("{n}", s.extra_needed);
  return t.enough;
}

function Pilgrim({ t, parking, best, shuttles, traffic, route }) {
  return (
    <>
      <h2>🚦 {t.traffic}</h2>
      {traffic.map((r) => (
        <div key={r.id} style={{ border: `3px solid ${r.closed ? "#6b7280" : tcolor[r.level]}`, borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <b>{t.roads[r.id] || r.name}</b>
          <p>{r.closed ? `🚧 ${t.closed}` : `${t.level[r.level]} ${t.trafficWord} | ~${r.time_min} ${t.min}`}</p>
        </div>
      ))}
      {route && route.recommended && (
        <div style={{ background: "#dbeafe", padding: 12, borderRadius: 8, marginBottom: 16 }}>
          🛣️ {t.recRoute}: <b>{t.roads[route.recommended.id] || route.recommended.name}</b> (~{route.recommended.time_min} {t.min})
        </div>
      )}

      <h2>{t.parkingStatus}</h2>
      {parking.map((p) => (
        <div key={p.id} style={{ border: `3px solid ${color[p.status]}`, borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{tr(t, p.name)}</h3>
          <p>{t.available}: {p.available} / {p.capacity} ({p.percent}% {t.full})</p>
          <b style={{ color: color[p.status] }}>{t.parkStatus[p.status]}</b>
        </div>
      ))}
      {best && best.name && (
        <div style={{ background: "#dcfce7", padding: 12, borderRadius: 8 }}>
          ✅ {t.recommended}: <b>{tr(t, best.name)}</b> ({best.available} {t.spacesFree})
        </div>
      )}
      {best && best.message && (
        <div style={{ background: "#fee2e2", padding: 12, borderRadius: 8 }}>⚠️ {t.allFull}</div>
      )}

      <h2>🚌 {t.shuttles}</h2>
      {shuttles.map((s) => (
        <div key={s.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{tr(t, s.name)}</h3>
          <p>{t.status}: <b>{t.shStatus[s.status]}</b> | {t.every} {s.interval_min} {t.min} | {s.running} {t.running}</p>
          <p>{t.waiting}: {s.waiting} | {t.demand}: <b style={{ color: dcolor[s.demand] }}>{t.demandL[s.demand]}</b></p>
        </div>
      ))}
    </>
  );
}

function SOS({ t }) {
  const [category, setCategory] = useState(CATEGORIES[2]);
  const [location, setLocation] = useState(LOCATIONS[0]);
  const [lat, setLat] = useState(null);
  const [lng, setLng] = useState(null);
  const [myId, setMyId] = useState(null);
  const [myReport, setMyReport] = useState(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (!myId) return;
    const timer = setInterval(async () => {
      try { setMyReport(await fetch(`${API}/sos/${myId}`).then((x) => x.json())); } catch { /* ignore */ }
    }, 3000);
    return () => clearInterval(timer);
  }, [myId]);

  const getGPS = () => {
    if (!navigator.geolocation) return setMsg(t.gpsNA);
    navigator.geolocation.getCurrentPosition(
      (pos) => { setLat(pos.coords.latitude); setLng(pos.coords.longitude); setMsg("📍 " + t.gpsOk); },
      () => setMsg(t.gpsDenied)
    );
  };

  const send = async () => {
    try {
      const res = await fetch(`${API}/sos`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category, location, lat, lng }),
      });
      if (!res.ok) throw new Error("failed");
      const data = await res.json();
      setMyId(data.id);
      setMyReport(data);
      setMsg("");
    } catch {
      setMsg("❌ " + t.notSent);
    }
  };

  return (
    <>
      <h2>🆘 {t.emergencyHelp}</h2>
      <p style={{ background: "#fee2e2", padding: 8, borderRadius: 6 }}><b>{t.call112}</b></p>
      <label>{t.emergencyType}</label>
      <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 10 }}>
        {CATEGORIES.map((c) => <option key={c} value={c}>{t.cat[c]}</option>)}
      </select>
      <label>{t.location}</label>
      <select value={location} onChange={(e) => setLocation(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 10 }}>
        {LOCATIONS.map((c) => <option key={c} value={c}>{t.loc[c]}</option>)}
      </select>
      <button onClick={getGPS} style={{ marginBottom: 10 }}>📍 {t.useGps}</button>
      {msg && <p>{msg}</p>}
      <button onClick={send} style={{ width: "100%", padding: 20, fontSize: 24, background: "#dc2626", color: "white", border: "none", borderRadius: 10, fontWeight: "bold" }}>
        🆘 {t.sendSos}
      </button>
      {myReport && (
        <div style={{ marginTop: 16, border: "2px solid #dc2626", borderRadius: 8, padding: 12 }}>
          <b>{t.report} #{myReport.id} {t.sent}</b> ({t.cat[myReport.category] || myReport.category}, {t.loc[myReport.location] || myReport.location})
          <div style={{ marginTop: 8 }}>
            {STATUSES.map((s, i) => (
              <div key={s} style={{ opacity: i <= STATUSES.indexOf(myReport.status) ? 1 : 0.3 }}>
                {i <= STATUSES.indexOf(myReport.status) ? "✅" : "⬜"} {t.sosStatus[s]}
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

function Admin({ t, parking, shuttles, traffic, reload }) {
  const [sos, setSos] = useState([]);

  const loadSos = async () => {
    try { setSos(await fetch(`${API}/sos`).then((r) => r.json())); } catch { /* ignore */ }
  };

  useEffect(() => {
    loadSos();
    const timer = setInterval(loadSos, 3000);
    return () => clearInterval(timer);
  }, []);

  const updateParking = async (id, occupied) => { await put(`/parking/${id}`, { occupied: Number(occupied) }); reload(); };
  const updateShuttle = async (id, body) => { await put(`/shuttle/${id}`, body); reload(); };
  const updateRoad = async (id, body) => { await put(`/traffic/${id}`, body); reload(); };
  const setStatus = async (id, status) => { await put(`/sos/${id}/status`, { status }); loadSos(); };

  return (
    <>
      <h2>🚨 {t.incidents}</h2>
      {sos.length === 0 && <p>{t.noIncidents}</p>}
      {sos.map((s) => (
        <div key={s.id} style={{ border: "2px solid #dc2626", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <b>#{s.id} {t.cat[s.category] || s.category}</b> — {t.loc[s.location] || s.location} ({s.time})
          {s.lat && <div>GPS: {s.lat.toFixed(5)}, {s.lng.toFixed(5)}</div>}
          <div style={{ marginTop: 6 }}>
            {t.status}:{" "}
            <select value={s.status} onChange={(e) => setStatus(s.id, e.target.value)}>
              {STATUSES.map((x) => <option key={x} value={x}>{t.sosStatus[x]}</option>)}
            </select>
          </div>
        </div>
      ))}

      <h2>🚦 {t.adminTraffic}</h2>
      {traffic.map((r) => (
        <div key={r.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <b>{t.roads[r.id] || r.name}</b>{" "}
          <select value={r.level} onChange={(e) => updateRoad(r.id, { level: e.target.value })}>
            {LEVELS.map((x) => <option key={x} value={x}>{t.level[x]}</option>)}
          </select>{" "}
          <label>
            <input type="checkbox" checked={r.closed} onChange={(e) => updateRoad(r.id, { closed: e.target.checked })} /> {t.closed}
          </label>
        </div>
      ))}

      <h2>🚌 {t.adminShuttles}</h2>
      {shuttles.map((s) => (
        <div key={s.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{tr(t, s.name)}</h3>
          <p>{t.waiting}: {s.waiting} | {t.demand}: <b style={{ color: dcolor[s.demand] }}>{t.demandL[s.demand]}</b></p>
          <input type="range" min="0" max="300" value={s.waiting}
            onChange={(e) => updateShuttle(s.id, { waiting: Number(e.target.value) })} style={{ width: "100%" }} />
          <p style={{ background: "#fef9c3", padding: 8, borderRadius: 6 }}>💡 {shuttleNote(t, s)}</p>
          <div>
            {t.runningShuttles}: <b>{s.running}</b>{" "}
            <button onClick={() => updateShuttle(s.id, { running: s.running + 1 })}>{t.assign}</button>{" "}
            <button onClick={() => updateShuttle(s.id, { running: Math.max(0, s.running - 1) })}>{t.remove}</button>
          </div>
          <div style={{ marginTop: 6 }}>
            {t.status}:{" "}
            <select value={s.status} onChange={(e) => updateShuttle(s.id, { status: e.target.value })}>
              {SHUTTLE_STATUSES.map((x) => <option key={x} value={x}>{t.shStatus[x]}</option>)}
            </select>
          </div>
        </div>
      ))}

      <h2>{t.adminParking}</h2>
      {parking.map((p) => (
        <div key={p.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{tr(t, p.name)}: {p.occupied} / {p.capacity}</h3>
          <input type="range" min="0" max={p.capacity} value={p.occupied}
            onChange={(e) => updateParking(p.id, e.target.value)} style={{ width: "100%" }} />
        </div>
      ))}
    </>
  );
}

export default function App() {
  const [lang, setLang] = useState(() => {
    try { return localStorage.getItem("lang") || "en"; } catch { return "en"; }
  });
  const [parking, setParking] = useState([]);
  const [best, setBest] = useState(null);
  const [shuttles, setShuttles] = useState([]);
  const [traffic, setTraffic] = useState([]);
  const [route, setRoute] = useState(null);
  const [view, setView] = useState("pilgrim");
  const t = T[lang];

  const changeLang = (l) => {
    setLang(l);
    try { localStorage.setItem("lang", l); } catch { /* ignore */ }
  };

  const load = async () => {
    try {
      setParking(await fetch(`${API}/parking`).then((r) => r.json()));
      setBest(await fetch(`${API}/parking/recommend`).then((r) => r.json()));
      setShuttles(await fetch(`${API}/shuttle`).then((r) => r.json()));
      setTraffic((await fetch(`${API}/traffic`).then((r) => r.json())).roads);
      setRoute(await fetch(`${API}/traffic/route`).then((r) => r.json()));
    } catch { /* ignore */ }
  };

  useEffect(() => {
    load();
    const timer = setInterval(load, 3000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20, fontFamily: "sans-serif", textAlign: "left" }}>
      <div style={{ textAlign: "right", marginBottom: 8 }}>
        {[["en", "English"], ["te", "తెలుగు"], ["hi", "हिन्दी"]].map(([k, label]) => (
          <button key={k} onClick={() => changeLang(k)}
            style={{ marginLeft: 6, fontWeight: lang === k ? "bold" : "normal", background: lang === k ? "#dbeafe" : undefined }}>
            {label}
          </button>
        ))}
      </div>
      <h1 style={{ fontSize: 28 }}>🚗 {t.title}</h1>
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setView("pilgrim")} style={{ marginRight: 8 }}>{t.pilgrim}</button>
        <button onClick={() => setView("sos")} style={{ marginRight: 8 }}>🆘 {t.sos}</button>
        <button onClick={() => setView("admin")}>{t.admin}</button>
      </div>
      {view === "pilgrim" && <Pilgrim t={t} parking={parking} best={best} shuttles={shuttles} traffic={traffic} route={route} />}
      {view === "sos" && <SOS t={t} />}
      {view === "admin" && <Admin t={t} parking={parking} shuttles={shuttles} traffic={traffic} reload={load} />}
    </div>
  );
}