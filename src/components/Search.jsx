import React from "react";

import AsyncSelect from "react-select/async";

class SelectSearch extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      tilds: null
    };
  }

  latestTild() {
    return this.state.tilds?.slice(-1)[0];
  }

  onChange = value => {
    this.setState({
      tilds: value
    });
  }

  loadOptions = (input) => {
    const node_id = this.latestTild()?.id ?? '';

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
          {this.latestTild()?.timestamp}
        </div>
      </div>
    );
  }
};

export default SelectSearch;