import {useState, useEffect} from 'react';
import LoadingPage from '../LoadingPage/LoadingPage';
import LoginRequired from '../LoginRequired/LoginRequired';
import RequestHandler from '../RequestHandler/RequestHandler';
import DashBoardPage from './DashBoardPage';
import {useNavigate} from 'react-router-dom';

// TODO:
//      Add vertical progress bars and graphs
//        style the running and diet sections


function DashBoard() {
    const [isLoggedIn, toggleLogIn] = useState<boolean>(false);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');

    const navigate = useNavigate();

    function validateSession(){
        toggleLoad(true);

        // get session data from local storage
        const userName: string = window.localStorage.getItem('username') || '';
        const token: string = window.localStorage.getItem('sessionToken') || '';


        RequestHandler.sendRequest('POST', 'check-session', {'username' : userName, 'token' : token}).then(
            (response) => {
                toggleLoad(false);

                if (response.success){
                    toggleLogIn(true);
                }else{
                    if (response.message === 'Profile Error'){
                        navigate('/profile');
                    }else{
                        setErrorMessage(response.message);
                    }
                }
            }
        )
    }


    useEffect(validateSession, []);


    return (
                isLoading ? <LoadingPage backgroundColor = 'white'/>
                    : isLoggedIn ? <DashBoardPage /> 
                        : <LoginRequired errorMessage = {errorMessage}/>
    );
}

export default DashBoard;