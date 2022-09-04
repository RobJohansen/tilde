import React from 'react';
import { render } from 'react-dom';

import Search from "./components/Search.jsx";

class App extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      node_id: null
    };

    this.handleSearchUpdate = this.handleSearchUpdate.bind(this)
  }

  handleTermsChange = (event) => {
    const node_id = this.state.node_id ?? '';
    const terms = event.target.value;

    console.log(node_id);
    console.log(terms);

    fetch(`search/page?node_id=${node_id}&terms=${terms}`)
      .then(response => response.json())
      .then(response =>
        console.log(response)
      );
  }

  handleSearchUpdate = (value) => {
    this.setState({
      node_id: value
    });

    console.log(value);
  }

  render() {
    return (
      <div>
        <input name="terms" onChange={this.handleTermsChange} />
        <Search handleSearchUpdate = {this.handleSearchUpdate} />
      </div>
    );
  }
}

render(<App />, document.getElementById('app'));