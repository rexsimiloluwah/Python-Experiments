import React from 'react';
import {Link} from 'react-router-dom'
import '../App.css';
import Header from './Header'

const Home = (props) => {
    return (
        <React.Fragment>
        <Header></Header>

        
        <div className = "container">
            <Link to="/blog"><button className="btn btn-warning">Go to Blog !</button></Link>
        </div>
        </React.Fragment>
    )
}

export default Home;