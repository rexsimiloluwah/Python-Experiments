import React from 'react';
import {BrowserRouter, Switch, Route} from 'react-router-dom'
import './App.css';
import Home from './components/Home'
import Blog from './components//Blog'
import BlogDetail from './components/BlogDetail'
import Category from './components/Category'

function App() {

  // useEffect( () => {
  //   axios.get('api/url')

  //   .then( (result) => {
  //     console.log(result)
  //   })

  //   .catch( (err) => {
  //     console.error(err)
  //   })
  // }, [])

  return (

    <React.Fragment>

      <BrowserRouter>

        <Switch>
          <Route exact path="/" component = {Home}></Route>
          <Route exact path="/blog" component = {Blog}></Route>
          <Route exact path="/blog/:id" component = {BlogDetail}></Route>
          <Route exact path="/category/:id" component = {Category}></Route>
        </Switch>

      </BrowserRouter>
    </React.Fragment>
    
  );
}

export default App;
