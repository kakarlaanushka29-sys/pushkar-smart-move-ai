import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";
const color = { AVAILABLE: "#22c55e", FILLING: "#eab308", FULL_RISK: "#ef4444" };

function Pilgrim({ parking, best }) {
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
    </>
  );
}

function Admin({ parking, reload }) {
  const update = async (id, occupied) => {
    await fetch(`${API}/parking/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ occupied: Number(occupied) }),
    });
    reload();
  };
  return (
    <>
      <h2>Admin: Update Parking</h2>
      {parking.map((p) => (
        <div key={p.id} style={{ border: "1px solid #999", borderRadius: 8, padding: 12, marginBottom: 12 }}>
          <h3>{p.name}: {p.occupied} / {p.capacity}</h3>
          <input
            type="range"
            min="0"
            max={p.capacity}
            value={p.occupied}
            onChange={(e) => update(p.id, e.target.value)}
            style={{ width: "100%" }}
          />
        </div>
      ))}
    </>
  );
}

export default function App() {
  const [parking, setParking] = useState([]);
  const [best, setBest] = useState(null);
  const [view, setView] = useState("pilgrim");

  const load = async () => {
    const p = await fetch(`${API}/parking`).then((r) => r.json());
    const b = await fetch(`${API}/parking/recommend`).then((r) => r.json());
    setParking(p);
    setBest(b);
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
        <button onClick={() => setView("admin")}>Admin View</button>
      </div>
      {view === "pilgrim" ? <Pilgrim parking={parking} best={best} /> : <Admin parking={parking} reload={load} />}
    </div>
  );
}