import React from 'react';
import axios from 'axios';
import Outputters from './Outputters.js';
import './cisco-atomic-ui.scss';
import Table from './Table.js';
import { Output } from './Output.js';
import {useState, useEffect} from 'react'
import SideBar from './SideBar.js';
import Header from './Header.js';
import ActivityGraph from './ActivityGraph.js';

class DataLake extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: '', lastWritten: []};
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
          <Header/>
          <div class="container-fluid">
            <div class="row semi-flexible">
            <div><SideBar/></div>
            <div>
            <div><ActivityGraph/></div>
	    <div class="col-md-12 content-container">
	      <div class="content"  >
	        <div class="row" >
                  <div class="col-md-12" >
                    <div class="panel"  >
                      <div class="table-admins">
                        <table class="table table--type-striped" >
              <thead>
                <tr>
                  <th colspan="8">
                    <div class="table__top-pane">
                      <div>
                        <div class="table__title">Security Data Lake Sources</div>
                      </div>
                    </div>
                  </th>
                </tr>
                <tr class="table__header-row">
                  <th class="table__header-cell">Format</th>
                  <th class="table__header-cell">Security Lake Source</th>
                  <th class="table__header-cell">S3 Bucket</th>
                  <th class="table__header-cell">Status</th>
                  <th class="table__header-cell">Bookmark</th>
                  <th class="table__header-cell"></th>
                </tr>
              </thead>
                           <tbody>
                             <tr class="table__row">
                               <td class="table__cell">{this.props.data.adapter}</td>
                               <td class="table__cell">{this.props.data.awssource}</td>
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
              </div>
              </div>
            </div>
          </div>
        </div>
      </body>
    );
  }
}

export default DataLake;
