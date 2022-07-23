import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import LoadingPage from "../LoadingPage/LoadingPage";
import LoginRequired from "../LoginRequired/LoginRequired";
import WorkoutsPage from "./WorkoutsPage";
import authenticate from '../Auth/Authentication';


export interface menuProps {
    toggleMode: (newMode: string) => any
}


function SavedWorkouts() {
    const [isLoggedIn, toggleLogIn] = useState<boolean>(false);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');

    const navigate = useNavigate();
    
    // eslint-disable-next-line react-hooks/exhaustive-deps
    useEffect(() => authenticate({ toggleLoad, toggleLogIn, navigate, setErrorMessage }), []);

    return (
        isLoading ? <LoadingPage backgroundColor='' />
            : isLoggedIn ? <WorkoutsPage />
                : <LoginRequired errorMessage={errorMessage} />
    );
}

export default SavedWorkouts;