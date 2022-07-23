import {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import LoadingPage from '../LoadingPage/LoadingPage';
import LoginRequired from '../LoginRequired/LoginRequired';
import DashBoardPage from './DashBoardPage';
import authenticate from '../Auth/Authentication';




function DashBoard() {
    const [isLoggedIn, toggleLogIn] = useState<boolean>(false);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');

    const navigate = useNavigate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    useEffect(() => authenticate({toggleLoad, toggleLogIn, navigate, setErrorMessage}), []);


    return (
                isLoading ? <LoadingPage backgroundColor = ''/>
                    : isLoggedIn ? <DashBoardPage /> 
                        : <LoginRequired errorMessage = {errorMessage}/>
    );
}

export default DashBoard;