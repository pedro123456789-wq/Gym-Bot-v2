import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import authenticate from "../Auth/Authentication";
import LoadingPage from "../LoadingPage/LoadingPage";
import LoginRequired from "../LoginRequired/LoginRequired";
import ProfilePage from "./ProfilePage";


function Profile() {
    const [isLoggedIn, toggleLogIn] = useState<boolean>(false);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');
    const navigate = useNavigate();

    useEffect(() => authenticate({ toggleLoad, toggleLogIn, navigate, setErrorMessage }), []);


    return (
        isLoading ? <LoadingPage backgroundColor='' />
            : isLoggedIn ? <ProfilePage />
                : <LoginRequired errorMessage={errorMessage} />
    );
}

export default Profile;