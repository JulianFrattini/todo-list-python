import React, { useState, useEffect } from 'react'
import './../Styles/TaskDetail.css'

import Editable from './Editable';

import Converter from './../Util/Converter'

function TaskDetail({ taskid, updateTasks }) {
    const [task, setTask] = useState(null);
    const [todos, setTodos] = useState([]);
    const [todo, setTodo] = useState("");

    useEffect(() => {
        updateTask();
    }, []);

    /**
     * Re-fetch the current task from the server once more
     */
    const updateTask = () => {
        fetch(`http://localhost:${process.env.REACT_APP_BACKEND_PORT}/tasks/byid/${taskid}`, {
            method: 'get',
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(tobj => {
                let converted = Converter.convertTask(tobj);
                setTask(converted);
                setTodos(converted.todos);
            })
            .catch(function (error) {
                console.error(error)
            });
    }

    /**
     * Add a todo item to the list
     * @param {*} e Event from the form submit
     */
    const addTodo = (e) => {
        e.preventDefault();

        const data = new URLSearchParams();
        data.append('taskid', task._id);
        data.append('description', todo);

        fetch(`http://localhost:${process.env.REACT_APP_BACKEND_PORT}/todos/create`, {
            method: 'post',
            body: data,
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(todoobj => updateTask())
            .then(updateTasks())
            .catch(function (error) {
                console.error(error)
            });

        
        setTodo("");
    }

    /**
     * Toggle the "done" status of a given todo object
     * @param {*} todo Todo object which is toggled
     */
    const toggleTodo = (todo) => {
        const data = new URLSearchParams();
        data.append('data', `{'$set': {'done': ${!todo.done}}}`);

        fetch(`http://localhost:${process.env.REACT_APP_BACKEND_PORT}/todos/byid/${todo._id}`, {
            method: 'put',
            body: data,
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(() => updateTask())
            .then(updateTasks())
            .catch(function (error) {
                console.error(error)
            });

    }

    /**
     * Delete an existing todo object
     * @param {*} todo Todo object which is deleted
     */
    const deleteTodo = (todo) => {
        fetch(`http://localhost:5000/todos/byid/${todo._id}`, {
            method: 'delete',
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(updateTask())
            .then(updateTasks())
            .catch(function (error) {
                console.error(error)
            });

    }

    return (
        task == null ?
            <p>Loading</p> :
            <div>
                <h1>
                    <Editable objectname="tasks" object={task} variablename="title" updateTasks={updateTasks} />
                </h1>

                <p>
                    <Editable objectname="tasks" object={task} variablename="description" updateTasks={updateTasks} />
                </p>

                <a href={`https://www.youtube.com/watch?v=${task.url}`} target='_blank' rel="noreferrer">
                    <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt='' />
                </a>
                <ul className='todo-list'>
                    {todos.map(todo =>
                        <li key={todo._id} className='todo-item'>
                            <span className={'checker ' + (todo.done ? 'checked' : 'unchecked')} onClick={() => toggleTodo(todo)}></span>
                            <Editable objectname="todos" object={todo} variablename="description" updateTasks={updateTasks} />
                            <span className='remover' onClick={() => deleteTodo(todo)}>&#x2716;</span>
                        </li>)
                    }
                    <li key='newtodo'>
                        <form onSubmit={addTodo} className='inline-form'>
                            <input type='text' onChange={e => setTodo(e.target.value)} value={todo} placeholder='Add a new todo item'></input>
                            <input type='submit' value='Add'></input>
                        </form>
                    </li>
                </ul>
            </div>
    );
}

export default TaskDetail