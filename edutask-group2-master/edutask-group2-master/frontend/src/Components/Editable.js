import React, {useState} from 'react'
import './../Styles/TaskDetail.css'

function Editable({ objectname, object, variablename, updateTasks }) {
    const [text, setText] = useState(object[variablename]);
    const [changing, setChanging] = useState(false);

    /**
     * Update the {variablename} attribute of {object} to the value {text}
     * @param {*} e Event triggered by the form submit
     */
    const save = (e) => {
        e.preventDefault();
        setChanging(false);
        
        // construct the form to submit
        const data = new URLSearchParams();
        data.append('data', `{'$set': {'${variablename}': '${text}'}}`);

        // send a request to the server updating the given field
        fetch(`http://localhost:5000/${objectname}/byid/${object._id}`, {
            method: 'put',
            body: data,
            headers: {'Cache-Control': 'no-cache'}
        })
            .then(res => res.json())
            .then(ob => updateTasks())
            .catch(function(error) {
                console.error(error)
            });
    }

    return (
        changing ? 
        <form onSubmit={save} className='inline-form'>                    
            <input type='text' onChange={e => setText(e.target.value)} value={text}></input>
            <input type='submit' value='Save'></input>
        </form>
        :
        <span onClick={() => setChanging(true)} className='editable'>{text}</span>
    );
}

export default Editable