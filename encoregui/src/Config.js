import React from 'react';
import FormHeader from './FormHeader';
import ActivityGraph from './ActivityGraph.js';
import axios from 'axios';
import Header from './Header.js';
import SideBar from './SideBar.js';
import Outputters from './Outputters.js';
import './cisco-atomic-ui.scss';
import Table from './Table.js';
import { Output } from './Output.js';
import {useState, useEffect} from 'react'

class Config extends React.Component {

  constructor(props) {
    super(props);
    this.state = {value: '', lastWritten: []};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getLastWritten = this.getLastWritten.bind(this);
    this.getStatus = this.getStatus.bind(this);

    this.awsRegion = React.createRef();
    this.awsAccount = React.createRef();
    this.awsS3 = React.createRef();
    this.certPass = React.createRef();
    this.awsSource = React.createRef();
    this.awsBufferRate = React.createRef();
  }

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

  afterSubmission(event) {
      event.preventDefault();
  }

  componentDidMount() {
    this.getLastWritten()
    this.getStatus()
  }

  handleChange(event) {
    event.preventDefault();
    this.setState({file: event.target.files[0]});
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
  }

  handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData();
    const awsRegion = this.awsRegion.current.value
    const awsAccount = this.awsAccount.current.value
    const awsS3 = this.awsS3.current.value
    const awsSource = this.awsSource.current.value
    const awsBufferRate = this.awsBufferRate.current.value

    var dict_t = [];
    dict_t = {"aws_region":awsRegion,"aws_account":awsAccount,"aws_s3":awsS3,"aws_buffer_rate":awsBufferRate,"aws_source":awsSource};

    try {
      axios({
        method: "post",
        url: "/api/modifyconfig/",
        data: dict_t,
        headers: { "Content-Type": "application/json"},
      });
    } catch(error) {
      console.log(error)
    }
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

  fileUploadForm(props) {
     const fileExists = 0;

     if (fileExists) {
       return <input id="certFile" type="file" onChange={this.handleChange} />;
     }
     else {
       return <input id="certFile" type="file" onChange={this.handleChange} />;
     }
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
                  <div class="col-md-12 content-container">
                    <h3>Setup Process</h3>
                    <div><FormHeader/></div>
                    <div class="panel">
                      <h3>Configuration</h3>
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
                                    {this.fileUploadForm(this.props)}
		                  </label>
		                </div>
		                <div class="form-group__text">
		                  <label class="label">
		                    AWS Account: &nbsp; &nbsp;
		                    <input id="awsAccount" ref={this.awsAccount} type="text" class="input" name="aws_account" placeholder={this.props.data.accountId}/>
		                  </label>
		                </div>
		                <div class="form-group__text">
		                  <label class="label">
		                    AWS Region: &nbsp; &nbsp;
		                  <input id="awsRegion" ref={this.awsRegion} type="text" class="input" name="aws_region" placeholder={this.props.data.region}/>
		                  </label>
		                </div>
                                <div class="form-group__text">
                                  <label class="label">
                                    AWS S3 Parition: &nbsp; &nbsp;
                                  <input id="awsS3" ref={this.awsS3} type="text" class="input" name="aws_s3"  placeholder={this.props.data.s3}/>
                                  <div class="help-block">
                                     <span class="help-block__text">Current Bucket:  {this.props.data.s3}</span>
                                  </div>
                                  </label>
                                </div>
                                <div class="form-group__text">
                                  <label class="label">
                                    AWS Data Lake Source: &nbsp; &nbsp;
                                  <input id="awsSource" ref={this.awsSource} type="text" class="input" name="aws_source" placeholder={this.props.data.awssource}/>
                                  <div class="help-block">
                                     <span class="help-block__text">Custom Security Lake Data Source</span>
                                  </div>
                                  </label>
                                </div>
                                <div class="form-group__text">
                                  <label class="label">
                                    Buffer Rate: &nbsp; &nbsp;
                                  <input id="awsBufferRate" ref={this.awsBufferRate} type="text" class="input" name="aws_buffer_rate" placeholder={this.props.data.awsBufferRate}/>
                                  <div class="help-block">
                                     <span class="help-block__text">Frequency which data is sent to AWS Security Lake (in secs)</span>
                                  </div>
                                  </label>
                                </div>
		                <input type="submit" class="btn btn--primary" value="Submit" />
		              </form>
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

export default Config;
