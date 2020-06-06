import React from 'react';
import ReactDOM from 'react-dom';

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
    this.setState({value: e.target.value});
  }

  handleKeyPress(e) {
    if (e.key == '~') {
      this.setState({tild: <Tild />});
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

class App extends React.Component {
  render() {
    return (
      <Search />
    );
  }
}

ReactDOM.render(
  <App />,
  document.getElementById('app')
);
