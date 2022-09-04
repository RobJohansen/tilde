import React from "react";

import AsyncSelect from "react-select/async";
import './../extensions';

class SelectSearch extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      tilds: null
    };
  }

  onChange = (value) => {
    this.setState({
      tilds: value
    });

    this.props.handleSearchUpdate(value.last()?.id);
  }

  loadOptions = (input) => {
    const node_id = this.state.tilds?.last()?.id ?? '';

    return fetch(`search?node_id=${node_id}&terms=${input}`)
      .then(response => response.json())
      .then(response => response.results);
  };

  render() {
    const { tilds } = this.state;

    return (
      <div>
        <AsyncSelect
          isMulti
          value={tilds}
          getOptionValue={e => e.id}
          getOptionLabel={e => e.name}
          onChange={this.onChange}
          loadOptions={this.loadOptions}
        />

        <div>
          {tilds?.map((tild) =>
            <span key={tild.id}>{tild.name}~</span>
          )}
        </div>

        <div>
          {this.state.tilds?.last()?.timestamp}
        </div>
      </div>
    );
  }
};

export default SelectSearch;