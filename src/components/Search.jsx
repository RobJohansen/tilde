import React from 'react';

import Tild from "./Tild.jsx";

class Search extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      tild: <Tild />
    };

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(e) {
    alert('A name was submitted: ' + this.state.tild);
    e.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        {this.state.tild}
        <input type="submit" value="Submit" />
      </form>
    )
  }
};

export default Search;