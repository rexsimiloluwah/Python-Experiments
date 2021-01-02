import React, {useState, useEffect} from 'react';
import '../App.css';
import {Container} from 'reactstrap';
import {Link} from 'react-router-dom';
import Comments from './Comments'
import axios from '../utilities/axios';

const BlogDetail = (props) => {

    const [blog, setBlog] = useState([])
    const [readingTime, setReadingTime] = useState([])

    const detailHeaderStyle = (img) => ({
        position: 'relative',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: '#fff',
        backgroundImage: `url(${img})`,
        linearGradient: 'rgba(255,0,0,0.45), rgba(255,0,0,0.45)',
        zIndex: 1,
        backgroundSize: 'cover',
        backgroundRepeat: 'round',
        width: '100%',
        height: '400px',
        objectFit: 'cover',
        opacity: 0.9
    })

    useEffect(() => {

        const slug = props.match.params.id
        
        axios.get(`posts/${slug}`)

        .then( (response) => {
            setBlog(response.data)
            // console.log(response.data.content.length)
            setReadingTime(response.data.content.length / 250)
        })
        .catch( (err) => {
            console.error(err)
        })

    }, [props.match.params.id])

    const createContent = () => {
        return {__html : blog.content}
    }

    return (
        <>
        <div className="detail-header" style= {detailHeaderStyle(blog.post_image)}>

            <div >
            <h1>{blog.title}</h1>
            <hr></hr>
            <p>
                <span><i className="bx bx-time"></i> {parseInt(readingTime)} minutes</span>
                <span className="mx-3"><i className="bx bx-user-circle"></i> TheBlackdove</span>
            </p>

            
            <div className="arrow-down">
                <i>↓</i>
            </div>
            </div>

        </div>

        <div className = "my-5">
            <Container>
                <p><button className="btn btn-warning">All</button>       <button className="mx-3 btn btn-warning">{blog.category}</button></p>
                <hr></hr>

                <p> <i className="bx bx-calendar"></i> { new Date("2020-06-06").toUTCString() }</p>

                <div className = "description">
                    {blog.description}
                </div>

                <p className = "content" dangerouslySetInnerHTML={createContent()}></p>

                <Link to = "/blog"><button className = "btn btn-warning">Back to Blogs ←</button></Link>


                <Comments fullUrl= {"https://mosimileoluwasblog.disqus.com/"}  id = {2} />
        

            </Container>
        </div>

        </>
    )
}

export default BlogDetail;
