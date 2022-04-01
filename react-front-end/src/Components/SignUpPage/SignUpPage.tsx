import Navbar from "../NavBar/Navbar";
import {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import RequestHandler from "../RequestHandler/RequestHandler";
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import Alert from "../Alert/Alert";


function SignUpPage() {
    // store user inputs
    const [userName, setUsername] = useState<string>();
    const [email, setEmail] = useState<string>();
    const [password, setPassword] = useState<string>();
    const [passwordConfirmation, setPasswordConfirmation] = useState<string>();

    // handle loading icon and alerts
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [showAlert, toggleAlert] = useState<boolean>(false);
    const [alertMessage, setMessage] = useState<string>('');
    const [isSuccess, toggleSuccess] = useState<boolean>(false);

    // react navigation
    const navigate = useNavigate();



    function createAccount(){
        // check if password confirmation  matches password 
        if (passwordConfirmation !== password){
            toggleAlert(true);
            setMessage('The two passwords do not match');
            toggleSuccess(false);

            // hide alert in 1 seconds
            setTimeout(() => toggleAlert(false), 1000);
            return;
        }

        toggleLoad(true);

        RequestHandler.Post('sign-up', {'username' : userName, 'password' : password, 'email' : email}).then(
            (response) => {
                toggleLoad(false);
                toggleAlert(true);
                setMessage(response.message);
                toggleSuccess(response.success);


                //hide alert after 1 second
                setTimeout(() => {
                    toggleAlert(false)
                    
                    // redirect user to email confirmation page once account is created
                    response.success && navigate('/confirm-email');
                }, 1000);
            }
        )
    }



    return (
        <div>
            <Navbar />

            <h1 className = 'text-center display-4'>
                Sign Up
            </h1>


            <div className = 'text-center mt-5'>
                {isLoading &&
                    <LoadingIndicator />
                }

                {showAlert && 
                    <Alert message = {alertMessage} isSuccess = {isSuccess} /> 
                }

                <form>
                    <div className = 'form-group'>
                        <label htmlFor = 'email'>Email</label>
                        
                        <div className = 'mt-4 mb-4'>
                            <input type = 'text' 
                                className = 'form-control text-center' 
                                id = 'email' 
                                style = {{width: '40vw', display: 'inline-block'}}
                                placeholder = 'Enter Email' 
                                onChange = {event => setEmail(event.target.value)}
                            />
                        </div>
                    </div>


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


                    <div className = 'form-group'>
                        <div className = 'mt-4 mb-4'>
                            <input type = 'password' 
                                className = 'form-control text-center' 
                                id = 'passwordConfirmation' 
                                placeholder = 'Confirm Password' 
                                style = {{width: '40vw', display: 'inline-block'}}
                                onChange = {event => setPasswordConfirmation(event.target.value)}
                            />
                        </div>
                    </div>

                    <button type = 'button' 
                            className = 'btn btn-dark btn-lg mt-3' 
                            style = {{width: '50vw'}}
                            onClick = {createAccount}>
                                Create Account
                    </button>
                </form>
            </div>
        </div>
    );
}

export default SignUpPage;