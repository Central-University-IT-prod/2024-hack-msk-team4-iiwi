import styles from "./Chart.module.scss";
import { PieChart } from "@mui/x-charts";

export function Chart() {
  return (
    <PieChart
      series={[
        {
          data: [
            {
              id: 0,
              value: 500,
              label: 'Должник 1',
            },
            {
              id: 0,
              value: 800,
              label: 'Должник 2',
            },
            {
              id: 0,
              value: 200,
              label: 'Должник 3',
            },
            {
              id: 0,
              value: 300,
              label: 'Должник 4',
            },
          ],
          innerRadius: 110,
          outerRadius: 150,
        },
      ]}
      width={800}
      height={500}
      className={styles.chart}
    />
  );
}
