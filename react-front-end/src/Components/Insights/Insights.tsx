import authenticate from "../Auth/Authentication";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingPage from "../LoadingPage/LoadingPage";
import LoginRequired from "../LoginRequired/LoginRequired";
import InsightsPage from "./InsightsPage";


function Insights() {
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const [isLoggedIn, toggleLogIn] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string>('');
    const navigate = useNavigate();

    useEffect(() => authenticate({ toggleLoad, toggleLogIn, navigate, setErrorMessage }), []);


    return (
        isLoading ? <LoadingPage backgroundColor="white" />
            : isLoggedIn ? <InsightsPage />
                : <LoginRequired errorMessage={errorMessage} />
    );
}

export default Insights;