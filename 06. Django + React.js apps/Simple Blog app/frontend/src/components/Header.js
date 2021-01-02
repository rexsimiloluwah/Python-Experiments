import React from 'react'
import {Container} from 'reactstrap'
import '../App.css'

const Header = (props) => {

    return(
        <Container className = "my-5">
            <div className = "header">
                <div className = "header-bg"></div>
                <div className="header-text">
                    <h1>Mosimileoluwa Okunowo</h1><hr></hr>
                    <p>Software Engineer     |     Artificial Intelligence enthusiast</p>
                </div>
                
            </div>

            <div className="social-icons">
                <a href="https://www.linkedin.com/in/similoluwa-okunowo-595787179/" target="blank"><i className="bx bxl-linkedin"></i></a>
                <a href="https://medium.com/@rexsimiloluwa" target="blank"><i className="bx bxl-medium"></i></a>
                <a href="https://twitter.com/Rexidic" target="blank"><i className="bx bxl-twitter"></i></a>
                <a href="https://twitter.com/Rexidic"><i className="bx bxl-github"></i></a>
            </div>
        </Container>
    )
}

export default Header;