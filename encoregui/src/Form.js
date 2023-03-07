import React from 'react';
import axios from 'axios';
import Outputters from './Outputters.js';
import './cisco-atomic-ui.scss';
import Table from './Table.js';
import { Output } from './Output.js';
import {useState, useEffect} from 'react'

class Form extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: '', lastWritten: []};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getLastWritten = this.getLastWritten.bind(this);
    this.getStatus = this.getStatus.bind(this);
  }

  handleChange(event) {    this.setState({file: event.target.files[0]});  }

  getLastWritten() {
    axios({
        method: "get",
        url: "/api/lastwritten/",
        headers: { "accept": "application/json", "Access-Control-Allow-Origin": "*"}
      }).then((response) => {
        this.state.lastWritten = response.data
        console.log(response.data)

      }).catch(err => console.log(err))
  }

  getStatus() {
    axios({
        method: "get",
        url: "/api/status/",
        headers: { "accept": "application/json", "Access-Control-Allow-Origin": "*"}
      }).then((response) => {
        this.state.status = response.data.state.description
        console.log(response.data)

      }).catch(err => console.log(err))
  }

  componentDidMount() {
    this.getLastWritten()
    this.getStatus()
  }
  handleSubmit(event) {
    const formData = new FormData();
    formData.append("file", this.state.file);
    try {
      axios({
        method: "post",
        url: "/api/uploadfile/",
        data: formData,
        headers: { "Content-Type": "multipart/form-data", "Access-Control-Allow-Origin": "*", "content": "application/json"},
      });
    } catch(error) {
      console.log(error)
    }
    alert('A name was submitted: ' + this.state.file);
    event.preventDefault();
  }

  handleStart(event) {

    try {
      axios({
        method: "post",
        url: "/api/execute/",
        headers: { "Content-Type": "multipart/form-data", "Access-Control-Allow-Origin": "*", "content": "application/json"},
      });
    } catch(error) {
      console.log(error)
    }
    alert('Running eNcore ');
    event.preventDefault();
  }

  handleStop(event) {

    try {
      axios({
        method: "post",
        url: "/api/executestop/",
        headers: { "Content-Type": "multipart/form-data", "Access-Control-Allow-Origin": "*", "content": "application/json"},
      });
    } catch(error) {
      console.log(error)
    }
    alert('Stopping eNcore ');
    event.preventDefault();
  }

  render() {

    return (
      <body class="atomic-ui-root">
        <div class="banner">
          <div class="form-group">
            <form onSubmit={this.handleSubmit}>
              <div class="form-group__text">
                <label class="label">
                  FMC URL: &nbsp; &nbsp;
                <input id="fmcUrl" type="text" class="input" name="fmcUrl" placeholder={this.props.data.host} />
                </label>
              </div>
              <div class="form-group__text">
                <label class="label">
                  FMC Certificate: &nbsp; &nbsp;    
                  <input type="file" onChange={this.handleChange} />
                  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
                  Password &nbsp; &nbsp;
                  <input type="password" />
                </label>
              </div>
              <div class="form-group__text">
                <label class="label">
                  AWS Account: &nbsp; &nbsp;
                  <input id="awsAccount" type="text" class="input" name="aws_account" placeholder={this.props.data.accountId}/>
                </label>
              </div>
              <div class="form-group__text">
                <label class="label">
                  AWS Region: &nbsp; &nbsp;
                <input id="awsRegion" type="text" class="input" name="aws_region" placeholder={this.props.data.region}/>
                </label>
              </div>
              <input type="submit" class="btn btn--primary" value="Submit" />
            </form>
          </div>
          <div>
            <div class="col-md-12">
              <div class="panel">
                <div class="table-admins">
                  <h3>Output Types</h3>
                  <table class="table">
                    <thead>
                      <tr class="table__header-row">
                        <th class="table__header-cell">Output Type</th>
                        <th class="table__header-cell">Local Path</th>
                        <th class="table__header-cell">S3 Bucket</th>
                        <th class="table__header-cell">Status</th>
                        <th class="table__header-cell">Bookmark</th>
                        <th class="table__header-cell">Action</th>
                      </tr>
                    </thead>
                     <tbody>
                       <tr class="table__row">
                       <td class="table__cell">{this.props.data.adapter}</td>
                       <td class="table__cell">{this.props.data.uri}</td>
                       <td class="table__cell">{this.props.data.s3}</td>
                       <td class="table__cell">{this.state.status}</td>
                       <td class="table__cell">{this.state.lastWritten}</td>
                       <td class="table__cell"><button class="btn btn--primary" onClick={this.handleStart}>Start</button><button class="btn btn--secondary" onClick={this.handleStop}>Stop</button></td></tr>
                     </tbody>
                   </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </body>
    );
  }
}

export default Form;
