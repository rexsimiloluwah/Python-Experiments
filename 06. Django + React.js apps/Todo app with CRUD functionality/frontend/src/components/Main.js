import React, {useState, useEffect} from 'react'
import '../App.css'
import axios from '../utilities/axios'
import Modal from './CustomModal'


const Main = (props) => {

    const [modal, setModal] = useState(false)
    const [tasks, setTasks] = useState([])
    const [editMode, setEditMode] = useState(false)

    const [activeItem, setActiveItem] = useState({
        id : "",
        title : "",
        description : "",
        completed : "",
        priority : ""
    })

    const toggle = () => (
        setModal(!modal)
    )

    const addTask = () => {

        setModal(!modal)
        setActiveItem(
            {
                id : "",
                title : "",
                description : "",
                completed : false,
                priority : ""
            }
        )
    }

    const refreshList = () => {

        axios.get("tasks")

        .then( (res) => {
            setTasks(res.data)

            setActiveItem(
                {
                    id : "",
                    title : "",
                    description : "",
                    completed : false,
                    priority : ""
                }
            )

            // console.log(res.data)
        })

        .catch( (err) => {
            console.error(err)
        })
    }

    const handleSubmit = async (task) => {

        toggle() 

        axios.post("tasks", task)

        .then( () => {
            refreshList()
        })

        .catch( (err) => {
            console.error(err)
        })
    }

    const editTask = async (task) => {

        toggle()

        setEditMode(false)

        axios.put(`tasks/${activeItem.id}`, task)

        .then( () => {
            refreshList()
        })

        .catch( (err) => {
            console.error(err)
        })
    }

    const handleEdit = (task) => {

        setActiveItem({
            id : task.id,
            title : task.title,
            description : task.description,
            priority : task.priority,
            completed : task.completed
        })


        toggle()

        setEditMode(true)

        // console.log(editMode)

    }

    useEffect( () => {

        refreshList()

    }, [])

    const handleDelete = (task) => {
        
        axios.delete(`tasks/${task.id}`)

        .then( (res) => {
            refreshList()
        })

    }

    
    return(
        <>

        <div className = "header">
            <div className = "hero container">
                
                <div className = "d-flex justify-content-center align-items-center">
                <div className = "hero-text my-3">
                    <h1 className = "text-center">Track your Tasks !</h1>
                    <hr></hr>
                    <p>Trackaa is a To-do list app that helps you keep track of your tasks for enhanced productivity !</p>
                </div> 
                </div>

                
                <div className = "hero-buttons d-flex justify-content-center flex-wrap-1">
                    <button className = "btn btn-success text-white m-2" onClick={() => addTask()}><i className="bx bx-plus"></i> Add a New Task</button>
                    <button className = "btn btn-danger text-white m-2"> <i className="bx bx-trash"></i> Delete All Tasks</button>
                </div>

            </div>
        </div>

        <div>
        <div className = "container my-5">
            <div className = "row vdivide">
                <div className = "col-md-8 incomplete">

                    <div className = "col-header">
                        <h4>Pending Tasks <span role="img" aria-label="pending">🙃</span></h4>
                    </div>
                    <hr></hr>

                    <ul>
                    {
                        tasks.filter( (obj) => { return !obj.completed }).map( (obj) => {
                        return(
                            <li key = {obj.id}>
                            <div className = "card task my-1">
                                <div className = "card-header">
                                    <input type="checkbox" name="checkbox" id="checkbox"></input>

                                    <span className = "title">{obj.title}</span>
                                    <span className= "edit-btn" onClick = {() => handleEdit(obj)}><i className = "bx bx-edit"></i></span>
                                    <span className = "delete-btn" onClick = {() => handleDelete(obj)}><i className = "bx bx-trash"></i></span>
                                </div>

                                <div className = "card-body">
                                    <small>{obj.description}</small>

                                    <span>
                                        <span className = "text-gray">{new Date(obj.timestamp).toDateString()}</span>
                                    </span>
                                </div>
                            </div>
                        </li>
                        )
                            

                        })
                    }  
                    </ul>
                    
                </div>

                <div className = "col-md-4 completed">

                    <div className = "col-header">
                        <h4>Completed Tasks <span role="img" aria-label="completed">🤩</span></h4>
                    </div><hr></hr>

                <ul>
                    {
                        tasks.filter( (obj) => { return obj.completed }).map( (obj) => {
                        return(
                            <li key = {obj.id}>
                            <div className = "card task my-1">
                                <div className = "card-header">
                                    <input type="checkbox" name="checkbox" id="checkbox" defaultChecked></input>

                                    <span className = "title">{obj.title}</span>
                                    <span className= "edit-btn" onClick = {() => handleEdit(obj)}><i className = "bx bx-edit"></i></span>
                                    <span className = "delete-btn" onClick = {() => handleDelete(obj)}><i className = "bx bx-trash"></i></span>
                                </div>

                                <div className = "card-body">
                                    <small>{obj.description}</small>

                                </div>
                            </div>
                        </li>
                        )
                            

                        })
                    }  
                    </ul>
                </div>
            </div>
        </div></div>

        <Modal toggle={toggle} modal={modal} addTask ={handleSubmit} activeTask = {activeItem} edit = {editTask} editMode = {editMode}></Modal>

        

        

        </>
    )
}

export default Main;