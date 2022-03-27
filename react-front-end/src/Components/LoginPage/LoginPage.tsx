import Navbar from "../NavBar/Navbar";
import {useState} from 'react';


function LoginPage() {
    const [username, setUsername] = useState<string>();
    const [password, setPassword] = useState<string>();
    
    function logIn(){

    }


    return (
        <div>
            <Navbar />
            
            <h1 className = 'text-center display-4'>
                Login
            </h1>

            <div className = 'text-center mt-5 pt-5'>
                <form>
                    <div className='form-group'>
                        <label htmlFor ='username'>Username</label>

                        <div className = 'mt-4 mb-4'>
                            <input type = 'text' 
                                id = 'username'
                                className = 'form-control text-center' 
                                placeholder ='Enter Username' 
                                style = {{width: '40vw', display: 'inline-block'}}
                                onChange = {event => setUsername(event.target.value)}
                            />
                        </div>
                    </div>
                    
                    <div className = 'form-group'>
                        <label htmlFor = 'password'>Password</label>
                        
                        <div className = 'mt-4 mb-4'>
                            <input type = 'password' 
                                className = 'form-control text-center' 
                                id = 'password' 
                                placeholder = 'Enter Password' 
                                style = {{width: '40vw', display: 'inline-block'}}
                                onChange = {event => setPassword(event.target.value)}
                            />
                        </div>
                    </div>

                    <button type = 'button' 
                            className = 'btn btn-dark btn-lg mt-5' 
                            style = {{width: '50vw'}}
                            onClick = {logIn}>
                                Log In
                    </button>
                </form>
            </div>
        </div>
    );
}

export default LoginPage;