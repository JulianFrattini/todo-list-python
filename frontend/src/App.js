import React, { useState } from 'react'
import './Styles/App.css'
import TaskView from './Components/TaskView'
import NavBar from './Components/NavBar'
import LoginForm from './Components/LoginForm'

function App() {
  const [user, setUser] = useState({})

  /**
   * Perform the signup of a new user
   * @param {*} details Dict containing at least the email, first name and last name of the new user
   */
  const signup = (details) => {
    // create a forms object
    const data = new URLSearchParams();
    data.append('email', details.email);
    data.append('firstName', details.firstName);
    data.append('lastName', details.lastName);

    // send a request to the server creating a new user
    fetch('http://localhost:5000/users/create', {
      method: 'post',
      body: data
    })
      .then(res => res.json())
      .then(userobj => {
        userobj['_id'] = userobj['_id']['$oid'];
        setUser(userobj);
      }).catch(function (error) {
        console.error(error)
      });
  }

  /**
   * Login to an existing account by providing the email address of an existing user
   * @param {*} details Dict contaiing at least the email address of a user
   */
  const login = (details) => {
    fetch(`http://localhost:5000/users/bymail/${details.email}`)
      .then(res => res.json())
      .then(userobj => {
        userobj['_id'] = userobj['_id']['$oid'];
        setUser(userobj);
      })
      .catch(function (error) {
        console.error(error)
      });
  }

  /**
   * Reset the authentication of the user
   */
  const logout = () => {
    setUser({});
  }

  return (
    <div>
      <NavBar Logout={logout} />

      <div className='main'>
        {(Object.keys(user).length === 0) ?
          <div>
            <h1>Login</h1>
            <LoginForm Login={login} Signup={signup} />
          </div>
          :
          <div>
            <h1>Your tasks, {user.firstName} {user.lastName}</h1>
            <TaskView user={user} />
          </div>}
      </div>
    </div>
  );
}

export default App