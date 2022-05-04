import Navbar from "../NavBar/Navbar";
import {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import RequestHandler from "../RequestHandler/RequestHandler";
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import Alert, { alertProps } from "../Alert/Alert";


function LoginPage() {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [showAlert, toggleAlert] = useState<boolean>(false);
    const [alertData, setAlertData] = useState<alertProps>({message: '', isSuccess: false});

    const navigate = useNavigate();
    

    function logIn(){
        // show loading indicator
        toggleLoad(true);

        RequestHandler.sendRequest('POST', 'log-in', {'username' : username, 'password' : password}).then(
            (response) => {
                // hide loading indicator once respone is recieved
                toggleLoad(false);
                toggleAlert(true);

                if (response.success){
                    setAlertData({message: 'Logged in successfully', isSuccess: true});

                    // store login token in local storage
                    window.localStorage.setItem('sessionToken', response.token)
                }else{
                    setAlertData({message: response.message, isSuccess: false})
                }
                
                
                // hide alert after 2 seconds 
                setTimeout(() => {
                    if (response.success){
                        // store session validation in local storage
                        const token = response.token
                        window.localStorage.setItem('sessionToken', token);
                        window.localStorage.setItem('username', username);

                        // redirect to dashboard page
                        navigate('/dashboard')
                    }
                    toggleAlert(false);
                }, 2000)
            }
        )
    }


    return (
        <div>
            <Navbar />
            
            <h1 className = 'text-center display-4'>
                Login
            </h1>

            <div className = 'text-center mt-5 pt-5'>
                {isLoading && <LoadingIndicator />}
                {showAlert && <Alert message = {alertData.message} isSuccess = {alertData.isSuccess} />}

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