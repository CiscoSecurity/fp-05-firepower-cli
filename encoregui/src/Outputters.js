import React from 'react';

class Outputters extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.handleStart = this.handleStart.bind(this);
  }

  handleStart(event) {    alert("Sending data to S3")  }

  render() {
    return (
            <div class="col-md-12">
              <div class="panel">
                <div class="table-admins">
                  <h3>Output Types</h3>
                  <table class="table">
                    <thead>
                      <tr class="table__header-row">
                        <th class="table__header-cell">Output Type</th>
                        <th class="table__header-cell">Destination</th>
                        <th class="table__header-cell table__header-cell--align-center">Active</th>
                        <th class="table__header-cell table__header-cell--align-right">Last Data Sent</th>
                        <th class="table__header-cell table__header-cell--align-right">Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr class="table__row">
                        <td class="table__cell">SPLUNK</td>
                        <td class="table__cell">/opt/splunk/etc/apps/TA-eStreamer/data/splunk</td>
			<td class="table__cell">Y</td>
                        <td class="table__cell table__cell--align-right">2/18/2023 13:44:44 PST</td>
			<td class="table__cell table__cell--align-right"><button class="btn btn--secondary">Stop</button></td>
                      </tr>
                      <tr class="table__row">
                        <td class="table__cell">JSON</td>
                        <td class="table__cell">relfile://data/json/</td>
			<td class="table__cell">N</td>
                        <td class="table__cell table__cell--align-right">1/18/2023 12:23:43 PST</td>
			<td class="table__cell table__cell--align-right"><button class="btn btn--secondary">Start</button></td>
                      </tr>
                      <tr class="table__row">
                        <td class="table__cell">OCSF</td>
                        <td class="table__cell">s3://aws-security-data-lake-us-east-2-351076683564</td>
                        <td class="table__cell">Y</td>
			<td class="table__cell table__cell--align-right">2/28/2023 09:33:33 PST</td>
                        <td class="table__cell table__cell--align-right"><button class="btn btn--secondary" onClick={this.handleStart}>Start</button></td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
    );
  }
}

export default Outputters;

