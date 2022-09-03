import React from 'react';
import { render } from 'react-dom';

import Search from "./components/Search.jsx";

class App extends React.Component {
  render() {
    return (
      <div>
        <Search />
      </div>
    );
  }
}

render(<App />, document.getElementById('app'));