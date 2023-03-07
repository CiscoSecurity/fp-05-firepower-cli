import React from 'react';
import axios from 'axios';

class FlavorForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: 'coconut'};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  uploadFile(event) {
      const file = event.target.files[0]
      alert('Filename: ' + file.name);
      axios.post("/uploadfile", file, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
      })
  }

  handleChange(event) {    this.setState({value: event.target.value});  }

  handleSubmit(event) {
    this.uploadFile(event)
    alert('Your favorite flavor is: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          Pick your favorite flavor:
          <select value={this.state.value} onChange={this.handleChange}>            <option value="grapefruit">Grapefruit</option>
            <option value="lime">Lime</option>
            <option value="coconut">Coconut</option>
            <option value="mango">Mango</option>
          </select>
        </label>
        <label for="myfile">Select a file:</label>
        <input type="file" id="file" name="file"/>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default FlavorForm;
