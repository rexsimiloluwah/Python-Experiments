import React, {useState, useRef} from 'react'
import '../App.css'
import {Modal, ModalHeader, ModalBody,Input} from 'reactstrap'


const CustomModal = (props) => {
  
  const {modal, 
    toggle,
    addTask,
    activeTask,
    editMode,
    edit
   } = props


   // States 
   const [title, setTitle] = useState("")
   const [description, setDescription] = useState("")
   const [completed, setCompleted] = useState(false)
   const [priority, setPriority] = useState("")

   const form = useRef(null)

   const handleTitleField = (e) => {
     setTitle(e.target.value)
   }

   const handleDescField = (e) => {
    setDescription(e.target.value)
  }

  const handlePriorityField = (e) => {
    setPriority(e.target.value)
  }

  const handleCompletedField = (e) => {
    setCompleted(e.target.checked)
  }

  const handleSubmit = (e) => {

    e.preventDefault()

    const formData = new FormData(e.target)

    let data = {}

    for (let [key, value] of formData.entries()) {
      data[key] = value
    }

    data["completed"] = data["completed"] === "on" ? true : completed
    data["title"] = data["title"].length > 0 ? data["title"] : title
    data["description"] = data["description"].length > 0 ? data["description"] : description
    data["priority"] = data["priority"].length > 0 ? data["priority"] : priority
    

    console.log(data)

    if(editMode){
      edit(data)
    }

    else{
      addTask(data)
    }

  }


  return (
    <div>
      <Modal isOpen={modal} toggle={toggle}>
        <ModalHeader toggle={toggle}>What do you want to do ?</ModalHeader>
        <ModalBody>
        <form ref = {form} onSubmit = {handleSubmit} >
            
            <div className = "form-group">
            <label for = "title">Title :</label>
            <input className = "form-control title" id="title" type="text" name = "title" defaultValue = {activeTask.title} placeholder = "Title of Task i.e. Read a Book" onChange = {handleTitleField}></input>
            </div>

            <div className = "form-group">
            <label for = "description">Description :</label>
            <input className = "form-control description" id = "description" name = "description" type = "text" defaultValue = {activeTask.description} placeholder = "Description of Task i.e. Complete the Machine learning book" onChange = {handleDescField}></input>
            </div>

            <div className = "form-group">
            <label for = "priority">Priority (or Urgency) :</label>
            <select className = "form-control priority" id = "priority" name = "priority" type = "select" defaultValue = {activeTask.priority} onChange = {handlePriorityField}>
              <option>High</option>
              <option>Normal</option>
              <option>Low</option>
            </select>
            </div>

            <div class="form-check">
            <input className="form-check-input completed" type="checkbox" value="" id="completed" name = "completed" defaultChecked={activeTask.completed} onChange={handleCompletedField}></input>
            <label class="form-check-label" for="completed">
              Completed ?
            </label>
            </div>

            <hr></hr>

            <Input type="submit"  value="Add/Edit Task" style={{backgroundColor:'#28a547', color:'#fff'}} ></Input>

        </form>

        </ModalBody>
        
        </Modal>
      
    </div>
  );
}

export default CustomModal;