import React, {useState, useEffect} from 'react';
import '../App.css';
import {Container, Col, Row, Card} from 'reactstrap';
import {Link} from 'react-router-dom';
import Header from './Header';
import axios from '../utilities/axios'

const Blog = (props) => {

    const [blogsData, setBlogsData] = useState([])

    useEffect( () => {
        axios.get('posts/')

        .then( (response) => {
            console.log(response.data)
            setBlogsData(response.data)
        })

        .catch( (err) => {
            console.error(err)
        })

    }, [])

    return(
        <React.Fragment>
        <Header></Header>

        <div>
            <Container>
                <div className = "blog-header">
                    <h1><span className="pretty-underline">My Blogs →</span>                    
                     </h1>

                     <ul className = "category-filter">
                        <li><Link to="/category/all">All</Link></li>
                        <li><Link to="/category/programming">Programming</Link></li>
                        <li><Link to="/category/technology">Technology</Link></li>
                    </ul>
                </div>

                <div className="blog-posts my-4">
                    <Row  className = "my-3">

                        {
                            blogsData.map( (obj) => {

                                return(
                                    <Col key = {obj.id} md="6">
                                    <Card className="blog-card">
                                    <img className="card-img" src={`${obj.post_image}`} alt=""></img>
                                    
                                    <div className="card-img-overlay">
                                        <a href="/" className="btn btn-light btn-sm">{obj.category}</a>
                                    </div>

                                    <div className = "card-body">
                                        <h4 className = "card-title">{obj.title}</h4>
                                        <small className = "text-muted">
                                            <span><i className = "bx bx-time"></i> {parseInt(obj.content.length/250)} minutes</span>
                                            <span className="mx-3"><i className = "bx bx-user-circle"></i> TheBlackdove</span>
                                        </small>

                                        <p className="blog-description">
                                            {obj.description.substr(0,200)+'...'}
                                        </p>

                                        <Link to= {`/blog/${obj.slug}`}><button className = "btn btn-warning" href="/">Read more →</button></Link>

                                        <hr></hr>
                                        <div className = "date_created">
                                            <p>{new Date(obj.timestamp).toUTCString()}</p>
                                        </div>
                                    </div>

                                    </Card>
                                    </Col>
                                )
                            })
                        }
                            
                    </Row>
                </div>
            </Container>
        </div>
        </React.Fragment>
    )
}

export default Blog;
