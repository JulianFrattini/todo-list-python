import React, { useState } from 'react'
import Converter from './../Util/Converter'

function TaskCreator(props) {
    const [title, setTitle] = useState("")
    const [url, setUrl] = useState("")

    /**
     * Create a new task with the {title} and {url}
     * @param {*} event Event object from the form submit
     */
    const submitNewTask = (event) => {
        event.preventDefault();

        // create a forms object
        const data = new URLSearchParams();
        data.append('title', title);
        data.append('description', '(add a description here)');
        data.append('userid', props.userid);
        data.append('url', url);
        data.append('todos', ['Watch video']);

        // reset the form values
        setTitle("");
        setUrl("");

        // send a request to the server creating the new task
        fetch('http://localhost:5000/tasks/create', {
            method: 'post',
            body: data
        }).then(res => res.json())
            .then(tasklist => {
                let convertedTasks = [];
                for (const task of tasklist) {
                    convertedTasks.push(Converter.convertTask(task));
                }
                props.setTasks(convertedTasks);
            })
            .catch(function (error) {
                console.error(error)
            });
    }

    return (
        <form className="submit-form bordered" onSubmit={submitNewTask}>
            <div className='inputwrapper'>
                <label>Title</label>
                <input type='text' id='title' name='title' onChange={event => setTitle(event.target.value)} value={title} placeholder='Title of your Task'></input>
            </div>
            <div className='inputwrapper'>
                <label>YouTube URL</label>
                <input type='text' id='url' name='url' onChange={event => setUrl(event.target.value)} value={url} placeholder='Viewkey of a YouTube video (the part after /watch?v= in the URL), e.g., dQw4w9WgXcQ'></input>
            </div>

            <input type="submit" value="Create new Task" disabled={title.length === 0}></input>
        </form>
    )
}

export default TaskCreator