import TargetsPage from "./TargetsPage";
import authenticate from "../Auth/Authentication";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingPage from "../LoadingPage/LoadingPage";
import LoginRequired from "../LoginRequired/LoginRequired";

function Targets() {
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [isLoggedIn, toggleLogIn] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');
    const navigate = useNavigate();

    useEffect(() => authenticate({ toggleLoad, toggleLogIn, navigate, setErrorMessage }), []);


    return (
        isLoading ? <LoadingPage backgroundColor="white" />
            : isLoggedIn ? <TargetsPage />
                : <LoginRequired errorMessage={errorMessage} />
    );
}

export default Targets;