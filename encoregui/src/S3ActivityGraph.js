import React from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PureComponent } from 'react';


class S3ActivityGraph extends PureComponent {
  constructor(props) {
    super(props);
    this.data = [ { name: "2023-05-19T05:39:31", uv: 203362, pv: 2400, amt: 2400 }, { name: "2023-05-19T05:40:31", uv: 371888, pv: 1398, amt: 2210 }, { name: "2023-05-19T05:50:31", uv: 122000, pv: 3333.23, amt: 2290 }, { name: "2023-05-19T06:40:31", uv: 144888, pv: 3908.44, amt: 2000 }, { name: "2023-05-19T07:40:31", uv: 1890, pv: 4800.11, amt: 2181 }, { name: "2023-05-19T08:40:31", uv: 55533, pv: 1144.4, amt: 2500 }, { name: "2023-05-19T09:40:31", uv: 112000, pv: 4300.11, amt: 2100 } ];
  }

  render() {

    return (
      <div>
        <h4>&nbsp;&nbsp;&nbsp;Data sent to S3 Security Lake (Total Events)</h4>
        <ResponsiveContainer height={200}>
          <AreaChart
            width={500}
            height={200}
            data={this.data}
            syncId="anyId"
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="uv" stroke="#8884d8" fill="#6A7890" />
          </AreaChart>
        </ResponsiveContainer>

      </div>
    );
  }
}

export default S3ActivityGraph;
