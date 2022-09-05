import React from 'react';

import Stack from "../types/Stack.jsx";

import { DateTime } from 'luxon';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';

import 'react-bootstrap-typeahead/css/Typeahead.css';

class Search extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      query: '',
      nodes: new Stack(),
      options: [],
      selected: [],
      isLoading: false
    };
  }

  updateParent = () => {
    const { query, nodes } = this.state;

    this.props.onSearchUpdate(
      query,
      nodes.peek()?.id
    );
  }

  onQueryUpdate = (event) => {
    this.setState({
      query: event.target.value
    }, this.updateParent);
  }

  renderMenuItemChildren = (option) => (
    <div key={option.id}>
      <span>{option.name}</span>
    </div>
  );

  onInputChange = (input) => {
    console.log(`input changed ${input}`);
  };

  onChange = (values) => {
    this.setState({
      selected: values
    });
  };

  onKeyDown = (event) => {
    const KEY_DELETE = 8;
    const KEY_ENTER = 13;
    const KEY_TILDE = 222;

    const { nodes, selected } = this.state;

    switch (event.keyCode) {
      case KEY_ENTER:
      case KEY_TILDE:
        event.preventDefault();

        if (selected.length > 0) {
          nodes.push(selected[0]);

          this.setState({
            nodes: nodes,
            selected: []
          }, this.updateParent);

          console.log(`push selected: ${selected[0]}`);
        }

        break;

      case KEY_DELETE:
        if (selected.length == 0 && !nodes.isEmpty()) {
          const node = nodes.pop();

          this.setState({
            nodes: nodes,
            selected: [node]
          }, this.updateParent);

          console.log(`pop node: ${node}`);
        }

        break;
    }
  };

  onSearch = (query) => {
    this.setState({
      isLoading: true
    });

    const parent_id = this.state.nodes.peek()?.id ?? '';

    fetch(`search/nodes?parent_id=${parent_id}&query=${query}`)
      .then(response => response.json())
      .then(response => this.setState({
        options: response.results,
        isLoading: false
      }));
  };

  render() {
    const { options, isLoading, selected, nodes } = this.state;

    const node = nodes.peek();
    const timestamp = node ? DateTime.fromHTTP(node.timestamp) : DateTime.now();

    return (
      <InputGroup>
        <Form.Control type="input" placeholder="Page..." onChange={this.onQueryUpdate} />

        <InputGroup.Text> ~ </InputGroup.Text>

        {
          nodes.items.map((node) =>
            <Button variant="outline-secondary" key={node.id}>~ {node.name}</Button>
          )
        }

        <AsyncTypeahead
          id="tilds"
          placeholder="Tilds..."
          minLength={2}
          useCache={false}
          labelKey="name"
          renderMenuItemChildren={this.renderMenuItemChildren}
          onInputChange={this.onInputChange}
          onKeyDown={this.onKeyDown}
          onChange={this.onChange}
          onSearch={this.onSearch}
          options={options}
          selected={selected}
          isLoading={isLoading}
          class="clearfix"
        />

        <InputGroup.Text>{timestamp.toFormat('yyyy-MM-dd')}</InputGroup.Text>

      </InputGroup>
    );
  }
};

export default Search;
