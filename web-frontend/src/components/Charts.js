import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

export default function Charts({ dataset }) {
  if (!dataset) return null;

  const typeData = {
    labels: Object.keys(dataset.type_distribution),
    datasets: [
      {
        label: "Equipment Count",
        data: Object.values(dataset.type_distribution),
        backgroundColor: "rgba(54, 162, 235, 0.7)",
      },
    ],
  };

  return (
    <div style={{ width: "600px", marginTop: "30px" }}>
      <h2>Equipment Type Distribution</h2>
      <Bar data={typeData} />
    </div>
  );
}
