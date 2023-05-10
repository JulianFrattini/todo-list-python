import React, { useState, useEffect } from 'react'
import './../Styles/TaskView.css'
import './../Styles/Form.css'
import Popup from './../Components/Popup'
import TaskDetail from './TaskDetail'
import TaskCreator from './TaskCreator'

import Converter from './../Util/Converter'

function TaskView(props) {

  const [tasks, setTasks] = useState([])
  const [focus, setFocus] = useState({})
  const [trigger, setTrigger] = useState(false)

  /**
   * At startup, retrieve all tasks of the registered user
   */
  useEffect(() => {
    updateTasks();
  }, []);

  /**
   * Fetch all tasks associated to this user from the server
   */
  const updateTasks = () => {
    fetch(`http://localhost:5000/tasks/ofuser/${props.user._id}`, {
      method: 'get',
      headers: { 'Cache-Control': 'no-cache' }
    })
      .then(res => res.json())
      .then(tasklist => {
        let convertedTasks = [];
        for (const task of tasklist) {
          convertedTasks.push(Converter.convertTask(task));
        }
        setTasks(convertedTasks);
      })
      .catch(function (error) {
        console.error(error)
      });
  }

  return (
    <div>
      {tasks.length === 0 ?
        <p>Here you find the space to organize the educational videos you are interested in and associate them with todo items. Start by pasting the view key of a YouTube video as well as a title of the task in the form below.</p>
        : <p>Here you can find your {tasks.length} task{tasks.length === 1 ? '' : 's'}. Click on each thumbnail in the list to add, update, or delete the todo items you have associated to this video.</p>}
      <div className='container'>
        {tasks.map(task =>
          <div className='container-element' key={task.id}>
            <a onClick={() => { setTrigger(true); setFocus(task) }}>
              <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt='' />
              { task.done ? <div className="done-overlay"><div className="done-check"></div></div> : <div></div>}
              <div className="title-overlay">{task.title}</div>
            </a>
          </div>)}

        <div className='container-element' key='newtask'>
          <TaskCreator userid={props.user._id} setTasks={setTasks} />
        </div>

        {trigger &&
          <Popup trigger={trigger} setTrigger={setTrigger}>
            <TaskDetail taskid={focus._id} updateTasks={updateTasks} />
          </Popup>
        }
      </div>
    </div>
  );
}

export default TaskView