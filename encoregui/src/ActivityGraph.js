import React from 'react'
import axios from 'axios';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { PureComponent } from 'react';


class ActivityGraph extends PureComponent {
  constructor(props) {
    super(props);
    this.state = {value: '', eventData: []};
    this.getEventRates = this.getEventRates.bind(this);
  }

  getEventRates() {
    axios({
        method: "get",
        url: "/api/datarate/",
        headers: { "accept": "application/json", "Access-Control-Allow-Origin": "*"}
      }).then((response) => {
        this.setState({ eventData : response.data })

      }).catch(err => console.log(err))
  }

  componentDidMount() {
    this.getEventRates()
  }

  render() {
    return (
      <div style={{ width: '85%' }}>
        <h4>&nbsp;&nbsp;&nbsp;Event Rate (per sec)</h4>

        <ResponsiveContainer height={200}>
          <AreaChart
            width={500}
            height={200}
            data={this.state.eventData}
            syncId="anyId"
            margin={{
              top: 10,
              right: 30,
              left: 0,
              bottom: 0,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="monitor" />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey="cumulative_rate" stroke="#82ca9d" fill="#005073" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    );
  }
}

export default ActivityGraph;
