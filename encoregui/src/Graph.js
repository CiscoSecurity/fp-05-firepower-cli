import React from 'react'
import { LineChart, Line } from 'recharts';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PureComponent } from 'react';


class ActivityGraph extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
        <ResponsiveContainer >
          <AreaChart height={400} data={this.props.graphData} margin={{top: 10, right: 30, left: 0, bottom: 0,}}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="uv" stackId="1" stroke="#8884d8" fill="#8884d8" />
            <Area type="monotone" dataKey="pv" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
            <Area type="monotone" dataKey="amt" stackId="1" stroke="#ffc658" fill="#ffc658" />
          </AreaChart>
        </ResponsiveContainer>
    );
  }
}

export default ActivityGraph;
