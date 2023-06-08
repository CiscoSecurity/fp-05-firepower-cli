import React from 'react';
import axios from 'axios';
import Outputters from './Outputters.js';
import './cisco-atomic-ui.scss';
import Table from './Table.js';
import { Output } from './Output.js';
import {useState, useEffect} from 'react'
import SideBar from './SideBar.js';
import Header from './Header.js';
import S3ActivityGraph from './S3ActivityGraph.js';

class Monitor extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: '', awsResponse: []};
    this.getAWSResponse = this.getAWSResponse.bind(this);
  }

  handleChange(event) {    this.setState({file: event.target.files[0]});  }

  getAWSResponse() {
    const formattedTasks = [];

    axios({
        method: "get",
        url: "/api/awsresponse/",
        headers: { "accept": "application/json", "Access-Control-Allow-Origin": "*"}
      }).then((response) => {
        this.state.awsResponse = Object.values(response.data)

        console.log(this.state.awsResponse)

      }).catch(err => console.log(err))
  }

  componentDidMount() {
    this.getAWSResponse()
  }

  render() {
    {/* Rendering hypen named columns can be tricky in REACT, we escape these in the API by for future ref: {response.HTTPHeaders['x-amz-request-id'] */}
    const s3URI = "s3://aws-security-data-lake/ext/CISCOFIREWALL/region=us-east-2/accountId=551076683564/eventDay=20230308/"
    return (
      <body class="atomic-ui-root" >
        <div class="banner" >
          <Header/>
          <div >
           <div >
            <div class="col-md-12 content-container" style={{ width: '200px', 'left': '0',position:'absolute' }} ><SideBar/></div>
            <div style={{ width: '1450px',top: '80px','right': '20px',position:'absolute' }} ><S3ActivityGraph/></div>
	    <div class="col-md-12 content-container" style={{ width: '1450px',top: '350px','right': '20px',position:'absolute' }} >
	      <div class="content" >
                  <div class="col-md-12" >
                    <div class="panel">
                      <div class="table-admins" >
                        <h3>Files Sent to AWS Security Lake</h3>
                        <table class="table">
                          <thead>
                            <th colspan="6"/>
                            <tr class="table__header-row">
                              <th class="table__header-cell">Request ID</th>
                              <th class="table__header-cell">Host ID</th>
                              <th class="table__header-cell">Filename</th>
                              <th class="table__header-cell">Transmitted</th>
                              <th class="table__header-cell">eTag</th>
                              <th class="table__header-cell">S3 URL</th>
                            </tr>
                           </thead>
                           <tbody>
                             {this.state.awsResponse.map((response) => (
                                 <tr class="table__row">
                                   <td class="table__cell">{response.RequestId}</td> 
                                   <td class="table__cell">{response.HostId}</td>
                                   <td class="table__cell">{response.Filename}</td>
                                   <td class="table__cell">{response.Transmitted}</td> 
                                   <td class="table__cell">{response.eTag}</td>
                                   <td class="table__cell"><a href={response.ObjectUrl} target="_blank"><span class="icon-link"></span></a></td>
                                 </tr>
                             ))}
                           </tbody>
                          </table>
                        </div> {/* table admins*/}
                      </div> {/* panel*/}
                    </div> {/* col md */}
                </div> {/* S3 Graph*/}
              </div>
            </div>
          </div>
        </div>
      </body>
    );
  }
}

export default Monitor;
