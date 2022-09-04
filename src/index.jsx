import React from 'react';
import { render } from 'react-dom';

import Search from "./components/Search.jsx";

class App extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      node_id: null,
      terms: null,
      url: null
    };

    this.handleSearchUpdate = this.handleSearchUpdate.bind(this)
  }

  handleTermsChange = (event) => {
    this.setState({
      terms: event.target.value
    }, this.update);
  }

  handleSearchUpdate = (value) => {
    this.setState({
      node_id: value
    }, this.update);
  }

  update = () => {
    const { node_id, terms } = this.state;

    if ((node_id ?? '') == '' || (terms ?? '') == '') {
      console.log(`clearing page`);

      this.setState({
        url: ''
      })
    } else {
      console.log(`updating page (node: ${node_id}, terms: ${terms})`);

      fetch(`search/terms?node_id=${node_id ?? ''}&terms=${terms}`)
        .then(response => response.json())
        .then(response =>
          this.setState({
            url: response.url
          })
        );
    }
  }

  render() {
    const { node_id, terms, url } = this.state;

    return (
      <div>
        <input name="terms" onChange={this.handleTermsChange} />

        <Search handleSearchUpdate={this.handleSearchUpdate} />

        <iframe src={url} width="100%" height="800px" ></iframe>
      </div>
    );
  }
}

render(<App />, document.getElementById('app'));