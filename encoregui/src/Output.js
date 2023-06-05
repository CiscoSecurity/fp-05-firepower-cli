import { LineChart, Line } from 'recharts';

const data = [{name: 'Page A', uv: 400, pv: 2400, amt: 2400}];

const renderLineChart = (
  <LineChart width={400} height={400} data={data}>
    <Line type="monotone" dataKey="uv" stroke="#8884d8" />
  </LineChart>
);

export function Output(props) {
  return (
    <tr class="table__row">
      <tr class="table__cell">{props.output.adapter}</tr>
      <tr class="table__cell">{props.output.stream[0].uri}</tr>
      <tr class="table__cell">{props.output.enabled}</tr>
      <button class="btn btn--primary">Run</button>
    </tr>
  );
}
