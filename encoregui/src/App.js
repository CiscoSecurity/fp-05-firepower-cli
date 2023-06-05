import './App.css';
import axios from 'axios';
import {useState, useEffect} from 'react'
import Form from './Form.js'
import Monitor from './Monitor.js'
import Config from './Config.js'
import Header from './Header.js'
import FormHeader from './FormHeader.js'
import DataLake from './DataLake.js'
import SideBar from './SideBar.js'
import Outputters from './Outputters.js'
import './cisco-atomic-ui.scss';
import {
  BrowserRouter as Router,
  Routes,
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

  return (
        <body class="atomic-ui-root">
        <Router>
          <Routes>
            <Route path ="/">
              <Route path ="/ocsf" element={<DataLake data={s3}/>}/>
              <Route path ="/monitor" element={<Monitor data={s3}/>}/>
              <Route path ="/config" element={<Config data={s3}/>}/>
            </Route>
          </Routes>
        </Router> 
	</body>
  );
}

export default App;
