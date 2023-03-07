import './App.css';
import axios from 'axios';
import {useState, useEffect} from 'react'
import Form from './Form.js'
import Header from './Header.js'
import FormHeader from './FormHeader.js'
import SideBar from './SideBar.js'
import Outputters from './Outputters.js'
import './cisco-atomic-ui.scss';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {

  const [config, setConfig] = useState([]);
  const [s3, setS3] = useState([])

  useEffect(() => {
    axios({
        method: "get",
        url: "/api/loadconfig/",
        headers: { "accept": "application/json", "Access-Control-Allow-Origin": "*"}
      }).then((response) => {
        setConfig(response.data.handler.outputters[0].adapter)
        const s3data =response.data.handler.outputters[0].stream.options 

        s3data["host"] = response.data.subscription.servers[0].host

        const outputs = [];
        for (let key in response.data.handler.outputters[0]) {

          s3data[key] = response.data.handler.outputters[0][key]

          for (let key in response.data.handler.outputters[0]["stream"]) {
            s3data[key] = response.data.handler.outputters[0]["stream"][key]
          }

        }

        setS3(s3data)

      }).catch(err => console.log(err))
      }, [])

  console.log(s3)
  return (
	<body class="atomic-ui-root">
	<div class="demo-page">
	    <Header />
          <div class="container-fluid">
	    <div class="row semi-flexible">
              <div><SideBar /></div>
              <div>
                <div class="col-md-12 content-container">
                  <div class="content">
                    <div class="row">
                      <div class="col-md-12">
                        <div><h2 class="content__title">Application Steps</h2></div>
                        <div><FormHeader /></div>
                      </div> 
                    </div>
                    <div class="row">
                      <div class="col-md-12">
                        <div class="panel user-profile">
                          <div><h2 class="content__title">Configuration Information</h2></div>
                          <Form data={s3}/>
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

export default App;
