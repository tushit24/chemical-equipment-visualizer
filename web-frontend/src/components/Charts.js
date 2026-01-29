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
        borderRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Equipment Type Distribution",
        font: {
          size: 16,
          weight: "bold",
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div
      style={{
        width: "100%",
        maxWidth: "700px",
        height: "400px",
        marginTop: "30px",
      }}
    >
      <Bar data={typeData} options={options} />
    </div>
  );
}
