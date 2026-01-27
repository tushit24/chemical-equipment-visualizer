import { useEffect, useState } from "react";
import API from "../api";
import Charts from "./Charts";

export default function HistoryTable() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("history/")
      .then((res) => setData(res.data))
      .catch((err) => console.error(err));
  }, []);

  const latest = data[0];

  return (
    <div>
      <h2>Uploaded Dataset History</h2>

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Filename</th>
            <th>Total</th>
            <th>Flowrate</th>
            <th>Pressure</th>
            <th>Temperature</th>
            <th>Uploaded At</th>
          </tr>
        </thead>
        <tbody>
          {data.map((d) => (
            <tr key={d.id}>
              <td>{d.filename}</td>
              <td>{d.total_equipment}</td>
              <td>{d.average_flowrate}</td>
              <td>{d.average_pressure}</td>
              <td>{d.average_temperature}</td>
              <td>{new Date(d.uploaded_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Chart Section */}
      <Charts dataset={latest} />
    </div>
  );
}
