import React, {useState} from 'react'
import './../Styles/Form.css'

function LoginForm({ Login, Signup }) {
    const [issignup, setIssignup] = useState(false);
    const [credentials, setCredentials] = useState({email: '', firstName: '', lastName: ''});

    /**
     * Take the stored credentials from the input and process them
     * @param {*} e Event from the form submit
     * @param {function} fun Either login or signup
     */
    const submitHandler = (e, fun) => {
        e.preventDefault();

        fun(credentials);
    }

    return (
        <form className="submit-form" onSubmit={(e) => submitHandler(e, (issignup ? Signup : Login))}>
            <div className='inputwrapper'>
                <label>Email Address</label>
                <input type='text' id='email' name='email' onChange={e => setCredentials({...credentials, email: e.target.value})} value={credentials.email}></input>
            </div>
            {issignup ? 
                <div>
                    <div className='inputwrapper'>
                        <label>First Name</label>
                        <input type='text' id='firstname' name='firstname' onChange={e => setCredentials({...credentials, firstName: e.target.value})} value={credentials.firstName}></input>
                    </div>
                    <div className='inputwrapper'>
                        <label>Last Name</label>
                        <input type='text' id='lastname' name='lastname' onChange={e => setCredentials({...credentials, lastName: e.target.value})} value={credentials.lastName}></input>
                    </div>
                </div>
                : 
                <div></div>}
            <div className='inputwrapper'>
                <label>Password</label>
                <input type='text' id='password' name='password' disabled placeholder='Password functionality not supported yet. Proceed the login/signup with the email address.'></input>
            </div>

            <input type="submit" value={issignup ? "Sign Up" : "Login"} disabled={credentials.email.length === 0}></input>

            { issignup ?  
            <a onClick={(e) => {e.preventDefault(); setIssignup(false)}}>Already have an account? Click here to log into an existing account.</a> :
            <a onClick={(e) => {e.preventDefault(); setIssignup(true)}}>Have no account yet? Click here to sign up.</a> }
        </form>
    );
}

export default LoginForm