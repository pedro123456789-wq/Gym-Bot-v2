import { Link } from "react-router-dom";
import Navbar from "../NavBar/Navbar";
const loginRequiredImage = require('../../Assets/loginRequired.png');


function LoginRequired({errorMessage} : {errorMessage : string}) {
    return (
        <div>
            <Navbar />

            <div className = 'text-center'>
                <h1 className = 'display-5 mt-5'>
                    Login required
                </h1>

                <p>{errorMessage}</p>
            </div>

            <div className = 'text-center mt-5'>
                <img src = {loginRequiredImage} className = 'login-required-image' alt = 'stop sign'></img>
            </div>
            
            <div className = 'text-center'>
                <Link className = 'btn btn-dark btn-lg text-center mt-5' 
                        to = '/log-in'
                        style = {{width: '20rem'}}>
                    Log In
                </Link>
            </div>
        </div>
    );
}

export default LoginRequired;