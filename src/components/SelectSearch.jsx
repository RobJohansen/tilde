import React from "react";

import AsyncSelect from "react-select/async";
import '../extensions';

class SelectSearch extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      nodes: null
    };
  }

  onChange = (value) => {
    this.setState({
      nodes: value
    });

    this.props.handleSearchUpdate(value.last()?.id);
  }

  loadOptions = (query) => {
    const parent_id = this.state.nodes?.last()?.id ?? '';

    return fetch(`search/nodes?parent_id=${parent_id}&query=${query}`)
      .then(response => response.json())
      .then(response => response.results);
  };

  render() {
    const { nodes } = this.state;

    return (
      <div>
        <AsyncSelect
          isMulti
          value={nodes}
          getOptionValue={e => e.id}
          getOptionLabel={e => e.name}
          onChange={this.onChange}
          loadOptions={this.loadOptions}
        />

        <div>
          {nodes?.map((node) =>
            <span key={node.id}>{node.name}~</span>
          )}
        </div>

        <div>
          {nodes?.last()?.timestamp}
        </div>
      </div>
    );
  }
};

export default SelectSearch;