import React, {useEffect, useState} from 'react'
import axios from '../utilities/axios'
import '../App.css'
import Header from './Header'
import {Link} from 'react-router-dom'
import {Row, Col, Card} from 'reactstrap'


const Category = (props) => {

    const [currentCategory, setCurrentCategory] = useState("")
    const [blogsData, setBlogsData] = useState([])

    useEffect( () => {

        const category = props.match.params.id

        if(category){
            let categoryList = document.querySelector('ul.category-filter')
            // console.log(categoryList.children)
            for (let i =0; i < categoryList.children.length ; i++){
                if (categoryList.children[i].classList.contains('active')){
                    categoryList.children[i].classList.remove('active')
                }
            }

            for (let i =0; i < categoryList.children.length ; i++){
                if (categoryList.children[i].textContent.toLowerCase() === category){
                    categoryList.children[i].classList.add('active')
                }
            }
        }

        setCurrentCategory(category)

        const config = {
             headers : {
                 'Content-type' : 'application/json'
             }
        }

        axios.post('/posts/category', {category}, config)

        .then( (res) => {
            setBlogsData(res.data)

        })

        .catch( (err) => {
            console.error(err)
        })
        

    }, [props.match.params.id])

    return(
        <>
        <div>
            
            <Header></Header>

            <div className = "container">
            <div className = "blog-header">
                <h1><span className="pretty-underline">My Blogs → </span>              
                </h1>

                    <ul className = "category-filter">
                    <li><Link to="/category/all">All</Link></li>
                    <li><Link to="/category/programming">Programming</Link></li>
                    <li><Link to="/category/technology">Technology</Link></li>
                </ul>
            </div>


            <div className="blog-posts my-4">
                    <Row className = "my-3">

                    {
                    blogsData.map( (obj) => {
                        return(
                            <Col key = {obj.id} md="6">
                            <Card className="blog-card my-3">
                            <img className="card-img" src = {obj.post_image} alt=""></img>
                            
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
            </div>
            
        </div>
        </>

    )
}

export default Category;