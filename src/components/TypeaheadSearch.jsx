import React from 'react';

import Stack from "../types/Stack.jsx";
import { AsyncTypeahead } from 'react-bootstrap-typeahead';

class TypeaheadSearch extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      nodes: new Stack(),
      options: [],
      selected: [],
      isLoading: false
    };
  }

  updateParent = () => {
    this.props.handleSearchUpdate(this.state.nodes.peek()?.id);
  }

  renderMenuItemChildren = (option) => (
    <div key={option.id}>
      <span>{option.name}</span>
    </div>
  );

  onInputChange = (input) => {
    console.log(`input changed ${input}`);
  };

  onChange = (value) => {
    this.setState({
      selected: value
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

    const parent_id = this.state.nodes?.peek()?.id ?? '';

    fetch(`search/nodes?parent_id=${parent_id}&query=${query}`)
      .then(response => response.json())
      .then(response => this.setState({
        options: response.results,
        isLoading: false
      }));
  };

  render() {
    const { options, isLoading, selected, nodes } = this.state;

    return (
      <div>
        <div>
          {nodes.items.map((node) =>
            <span key={node.id}>~{node.name}</span>
          )}
        </div>

        <AsyncTypeahead
          id="search"
          placeholder="Search..."
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
        />

        <div>
          {nodes?.peek()?.timestamp}
        </div>
      </div>
    );
  }
};

export default TypeaheadSearch;
