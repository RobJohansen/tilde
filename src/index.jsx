import React from 'react';
import { render } from 'react-dom';

import TypeaheadSearch from "./components/TypeaheadSearch.jsx";

class App extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      node_id: null,
      query: null,
      page_url: null
    };

    this.handleSearchUpdate = this.handleSearchUpdate.bind(this)
  }

  handleSearchUpdate = (value) => {
    this.setState({
      node_id: value
    }, this.updatePage);
  }

  handleQueryChange = (event) => {
    this.setState({
      query: event.target.value
    }, this.updatePage);
  }

  updatePage = () => {
    const { node_id, query } = this.state;

    if ((node_id ?? '') == '' || (query ?? '') == '') {
      console.log(`clearing page`);

      this.setState({
        page_url: ''
      })
    } else {
      console.log(`updating page (node: ${node_id}, query: ${query})`);

      fetch(`search/page?node_id=${node_id}&query=${query}`)
        .then(response => response.json())
        .then(response =>
          this.setState({
            page_url: response.page_url
          })
        );
    }
  }

  render() {
    const { page_url } = this.state;

    return (
      <div>
        <input name="query" onChange={this.handleQueryChange} />
        <TypeaheadSearch handleSearchUpdate={this.handleSearchUpdate} />

        <iframe src={page_url} width="100%" height="800px" ></iframe>
      </div>
    );
  }
}

render(<App />, document.getElementById('app'));