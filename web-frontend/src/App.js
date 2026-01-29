import { useRef } from "react";
import CSVUpload from "./components/CSVUpload";
import HistoryTable from "./components/HistoryTable";

function App() {
  const historyRef = useRef();

  return (
    <div style={{ padding: "30px", background: "#f4f6f9", minHeight: "100vh" }}>
      <h1 style={{ textAlign: "center" }}>
        Chemical Equipment Parameter Visualizer
      </h1>
      <p style={{ textAlign: "center", color: "#555" }}>
        Upload, analyze, visualize & export equipment datasets
      </p>

      {/* ✅ CSV Upload */}
      <CSVUpload onUploadSuccess={() => historyRef.current?.refresh()} />

      {/* ✅ History + Charts */}
      <HistoryTable ref={historyRef} />
    </div>
  );
}

export default App;
