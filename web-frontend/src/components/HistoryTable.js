import {
  useEffect,
  useState,
  forwardRef,
  useImperativeHandle,
} from "react";
import API from "../api";
import Charts from "./Charts";
import "./HistoryTable.css";

const HistoryTable = forwardRef((props, ref) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = () => {
    setLoading(true);
    API.get("history/")
      .then((res) => setData(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  // 🔑 Expose refresh() to parent (App.js)
  useImperativeHandle(ref, () => ({
    refresh: fetchHistory,
  }));

  useEffect(() => {
    fetchHistory();
  }, []);

  const latest = data[0];

  const downloadPDF = async (id) => {
    try {
      const response = await API.get(`pdf/${id}/`, {
        responseType: "blob",
      });

      const blob = new Blob([response.data], {
        type: "application/pdf",
      });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = `dataset_${id}_report.pdf`;
      document.body.appendChild(link);
      link.click();

      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Failed to download PDF");
      console.error(err);
    }
  };

  return (
    <div className="card">
      <h2>Uploaded Dataset History</h2>

      {/* Non-blocking loading */}
      {loading && (
        <p style={{ textAlign: "center", color: "#777" }}>
          Loading datasets…
        </p>
      )}

      {/* Empty state */}
      {!loading && data.length === 0 && (
        <p style={{ textAlign: "center", color: "#777" }}>
          No datasets uploaded yet.
        </p>
      )}

      {data.length > 0 && (
        <>
          <div className="table-wrapper">
            <table className="styled-table">
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Total</th>
                  <th>Flowrate</th>
                  <th>Pressure</th>
                  <th>Temperature</th>
                  <th>Uploaded At</th>
                  <th>PDF</th>
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
                    <td>
                      <button
                        className="btn btn-secondary"
                        onClick={() => downloadPDF(d.id)}
                      >
                        Download PDF
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Chart */}
          {latest && (
            <div className="chart-container">
              <Charts dataset={latest} />
            </div>
          )}
        </>
      )}
    </div>
  );
});

export default HistoryTable;
