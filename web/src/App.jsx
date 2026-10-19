import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";
const color = { AVAILABLE: "#22c55e", FILLING: "#eab308", FULL_RISK: "#ef4444" };
const dcolor = { LOW: "#22c55e", MEDIUM: "#eab308", HIGH: "#ef4444" };
const STATUSES = ["Reported", "Acknowledged", "Team Assigned", "Help Arrived", "Resolved"];
const CATEGORIES = ["Accident", "Injured pilgrim", "Medical emergency", "Missing person", "Crowd emergency", "Other"];
const LOCATIONS = ["Ghat A", "Ghat B", "Entry Gate C", "Parking A", "Parking B"];
const SHUTTLE_STATUSES = ["Running", "Delayed", "Disrupted"];
const put = (url, body) =>
  fetch(`${API}${url}`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

function Pilgrim({ parking, best, shuttles }) {
  return (
    <>
      <h2>Parking Status</h2>
      {parking.map((p) => (
        <div key={p.id} style={{ border: `3px solid ${color[p.status]}`, borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{p.name}</h3>
          <p>Available: {p.available} / {p.capacity} ({p.percent}% full)</p>
          <b style={{ color: color[p.status] }}>{p.status}</b>
        </div>
      ))}
      {best && best.name && (
        <div style={{ background: "#dcfce7", padding: 12, borderRadius: 8 }}>
          ✅ Recommended: <b>{best.name}</b> ({best.available} spaces free)
        </div>
      )}
      <h2>🚌 Shuttles to Ghat</h2>
      {shuttles.map((s) => (
        <div key={s.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{s.name}</h3>
          <p>Status: <b>{s.status}</b> | Every {s.interval_min} min | {s.running} shuttle(s) running</p>
          <p>Waiting: {s.waiting} | Demand: <b style={{ color: dcolor[s.demand] }}>{s.demand}</b></p>
        </div>
      ))}
    </>
  );
}

function SOS() {
  const [category, setCategory] = useState(CATEGORIES[2]);
  const [location, setLocation] = useState(LOCATIONS[0]);
  const [lat, setLat] = useState(null);
  const [lng, setLng] = useState(null);
  const [myId, setMyId] = useState(null);
  const [myReport, setMyReport] = useState(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    if (!myId) return;
    const t = setInterval(async () => {
      try {
        setMyReport(await fetch(`${API}/sos/${myId}`).then((x) => x.json()));
      } catch { /* ignore */ }
    }, 3000);
    return () => clearInterval(t);
  }, [myId]);

  const getGPS = () => {
    if (!navigator.geolocation) return setMsg("GPS not supported. Select location manually.");
    navigator.geolocation.getCurrentPosition(
      (pos) => { setLat(pos.coords.latitude); setLng(pos.coords.longitude); setMsg("📍 GPS location captured"); },
      () => setMsg("GPS denied. Please select location manually.")
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
      setMsg("❌ Report NOT sent. Call 112 now!");
    }
  };

  return (
    <>
      <h2>🆘 Emergency Help</h2>
      <p style={{ background: "#fee2e2", padding: 8, borderRadius: 6 }}>
        Life-threatening emergency? <b>Call 112 immediately.</b>
      </p>
      <label>Emergency type</label>
      <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 10 }}>
        {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
      </select>
      <label>Location</label>
      <select value={location} onChange={(e) => setLocation(e.target.value)} style={{ width: "100%", padding: 8, marginBottom: 10 }}>
        {LOCATIONS.map((c) => <option key={c}>{c}</option>)}
      </select>
      <button onClick={getGPS} style={{ marginBottom: 10 }}>📍 Use my GPS (optional)</button>
      {msg && <p>{msg}</p>}
      <button onClick={send} style={{ width: "100%", padding: 20, fontSize: 24, background: "#dc2626", color: "white", border: "none", borderRadius: 10, fontWeight: "bold" }}>
        🆘 SEND SOS
      </button>
      {myReport && (
        <div style={{ marginTop: 16, border: "2px solid #dc2626", borderRadius: 8, padding: 12 }}>
          <b>Report #{myReport.id} sent</b> ({myReport.category} at {myReport.location})
          <div style={{ marginTop: 8 }}>
            {STATUSES.map((s, i) => (
              <div key={s} style={{ opacity: i <= STATUSES.indexOf(myReport.status) ? 1 : 0.3 }}>
                {i <= STATUSES.indexOf(myReport.status) ? "✅" : "⬜"} {s}
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

function Admin({ parking, shuttles, reload }) {
  const [sos, setSos] = useState([]);

  const loadSos = async () => {
    try { setSos(await fetch(`${API}/sos`).then((r) => r.json())); } catch { /* ignore */ }
  };

  useEffect(() => {
    loadSos();
    const t = setInterval(loadSos, 3000);
    return () => clearInterval(t);
  }, []);

  const updateParking = async (id, occupied) => { await put(`/parking/${id}`, { occupied: Number(occupied) }); reload(); };
  const updateShuttle = async (id, body) => { await put(`/shuttle/${id}`, body); reload(); };
  const setStatus = async (id, status) => { await put(`/sos/${id}/status`, { status }); loadSos(); };

  return (
    <>
      <h2>🚨 Emergency Incidents</h2>
      {sos.length === 0 && <p>No incidents.</p>}
      {sos.map((s) => (
        <div key={s.id} style={{ border: "2px solid #dc2626", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <b>#{s.id} {s.category}</b> at {s.location} ({s.time})
          {s.lat && <div>GPS: {s.lat.toFixed(5)}, {s.lng.toFixed(5)}</div>}
          <div style={{ marginTop: 6 }}>
            Status:{" "}
            <select value={s.status} onChange={(e) => setStatus(s.id, e.target.value)}>
              {STATUSES.map((x) => <option key={x}>{x}</option>)}
            </select>
          </div>
        </div>
      ))}

      <h2>🚌 Admin: Shuttles (simulated data)</h2>
      {shuttles.map((s) => (
        <div key={s.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{s.name}</h3>
          <p>Waiting: {s.waiting} | Demand: <b style={{ color: dcolor[s.demand] }}>{s.demand}</b></p>
          <input type="range" min="0" max="300" value={s.waiting}
            onChange={(e) => updateShuttle(s.id, { waiting: Number(e.target.value) })} style={{ width: "100%" }} />
          <p style={{ background: "#fef9c3", padding: 8, borderRadius: 6 }}>💡 {s.suggestion}</p>
          <div>
            Running shuttles: <b>{s.running}</b>{" "}
            <button onClick={() => updateShuttle(s.id, { running: s.running + 1 })}>+ Assign</button>{" "}
            <button onClick={() => updateShuttle(s.id, { running: Math.max(0, s.running - 1) })}>- Remove</button>
          </div>
          <div style={{ marginTop: 6 }}>
            Status:{" "}
            <select value={s.status} onChange={(e) => updateShuttle(s.id, { status: e.target.value })}>
              {SHUTTLE_STATUSES.map((x) => <option key={x}>{x}</option>)}
            </select>
          </div>
        </div>
      ))}

      <h2>Admin: Update Parking</h2>
      {parking.map((p) => (
        <div key={p.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{p.name}: {p.occupied} / {p.capacity}</h3>
          <input type="range" min="0" max={p.capacity} value={p.occupied}
            onChange={(e) => updateParking(p.id, e.target.value)} style={{ width: "100%" }} />
        </div>
      ))}
    </>
  );
}

export default function App() {
  const [parking, setParking] = useState([]);
  const [best, setBest] = useState(null);
  const [shuttles, setShuttles] = useState([]);
  const [view, setView] = useState("pilgrim");

  const load = async () => {
    try {
      setParking(await fetch(`${API}/parking`).then((r) => r.json()));
      setBest(await fetch(`${API}/parking/recommend`).then((r) => r.json()));
      setShuttles(await fetch(`${API}/shuttle`).then((r) => r.json()));
    } catch { /* ignore */ }
  };

  useEffect(() => {
    load();
    const t = setInterval(load, 3000);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20, fontFamily: "sans-serif", textAlign: "left" }}>
      <h1 style={{ fontSize: 28 }}>🚗 Pushkar Smart Move AI</h1>
      <div style={{ marginBottom: 16 }}>
        <button onClick={() => setView("pilgrim")} style={{ marginRight: 8 }}>Pilgrim View</button>
        <button onClick={() => setView("sos")} style={{ marginRight: 8 }}>🆘 SOS</button>
        <button onClick={() => setView("admin")}>Admin View</button>
      </div>
      {view === "pilgrim" && <Pilgrim parking={parking} best={best} shuttles={shuttles} />}
      {view === "sos" && <SOS />}
      {view === "admin" && <Admin parking={parking} shuttles={shuttles} reload={load} />}
    </div>
  );
}