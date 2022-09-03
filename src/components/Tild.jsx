import React from 'react';

class Tild extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      value: '',
      tild: null
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  handleKeyPress(e) {
    if (e.key == '~') {
      this.setState({ tild: <Tild /> });
      e.preventDefault();
    }
  }

  render() {
    return (
      <span>
        <input
          type="text"
          value={this.state.value}
          onChange={this.handleChange}
          onKeyPress={this.handleKeyPress} />
        {this.state.tild}
      </span>
    )
  }
};

export default Tild;