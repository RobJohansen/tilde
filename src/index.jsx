import React from 'react';
import { render } from 'react-dom';

import Search from "./components/Search.jsx";

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import 'bootstrap/dist/css/bootstrap.css';

class App extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      query: null,
      node_id: null,
      page_url: null
    };

    this.onSearchUpdate = this.onSearchUpdate.bind(this)
  }

  onSearchUpdate = (query, node_id) => {
    this.setState({
      query: query,
      node_id: node_id
    });

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
      <Container>
        <Row>
          <Search onSearchUpdate={this.onSearchUpdate} />
        </Row>
        <Row>
          <iframe src={page_url} width="100%" height="800px" border="0" ></iframe>
        </Row>
      </Container>
    );
  }
}

render(<App />, document.getElementById('app'));