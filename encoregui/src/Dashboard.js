import React from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PureComponent } from 'react';


class Dashboard extends PureComponent {
  constructor(props) {
    super(props);
//    this.data = [ { name: "2023-05-19T05:39:31", uv: 203362, pv: 2400, amt: 2400 }, { name: "2023-05-19T05:40:31", uv: 371888, pv: 1398, amt: 2210 }, { name: "2023-05-19T05:50:31", uv: 122000, pv: 3333.23, amt: 2290 }, { name: "2023-05-19T06:40:31", uv: 144888, pv: 3908.44, amt: 2000 }, { name: "2023-05-19T07:40:31", uv: 1890, pv: 4800.11, amt: 2181 }, { name: "2023-05-19T08:40:31", uv: 55533, pv: 1144.4, amt: 2500 }, { name: "2023-05-19T09:40:31", uv: 112000, pv: 4300.11, amt: 2100 } ];
this.data = [
  {
    month: '2015.01',
    a: 4000,
    b: 2400,
    c: 2400,
  },
  {
    month: '2015.02',
    a: 3000,
    b: 1398,
    c: 2210,
  },
  {
    month: '2015.03',
    a: 2000,
    b: 9800,
    c: 2290,
  },
  {
    month: '2015.04',
    a: 2780,
    b: 3908,
    c: 2000,
  },
  {
    month: '2015.05',
    a: 1890,
    b: 4800,
    c: 2181,
  },
  {
    month: '2015.06',
    a: 2390,
    b: 3800,
    c: 2500,
  },
  {
    month: '2015.07',
    a: 3490,
    b: 4300,
    c: 2100,
  },
];

  }

  render() {

    return (
      <div style={{ width: '85%' }}>
        <h4>&nbsp;&nbsp;&nbsp;Data sent to S3 Security Lake (Total Events)</h4>
        <ResponsiveContainer width={'95%'} height={200}>
          <AreaChart
            width={500}
            height={400}
            data={data}
            stackOffset="expand"
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis tickFormatter={toPercent} />
            <Tooltip content={renderTooltipContent} />
            <Area type="monotone" dataKey="a" stackId="1" stroke="#8884d8" fill="#8884d8" />
            <Area type="monotone" dataKey="b" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
            <Area type="monotone" dataKey="c" stackId="1" stroke="#ffc658" fill="#ffc658" />
          </AreaChart>
        </ResponsiveContainer>

      </div>
    );
  }
}

export default Dashboard;
