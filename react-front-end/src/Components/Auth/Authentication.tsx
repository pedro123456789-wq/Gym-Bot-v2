import { useState, createContext } from "react";
import RequestHandler from "../RequestHandler/RequestHandler";



interface authProps {
    toggleLoad: (arg0: boolean) => any,
    toggleLogIn: (arg0: boolean) => any,
    navigate: (arg0: string) => any,
    setErrorMessage: (arg0: string) => any
}


function authenticate({ toggleLoad, toggleLogIn, navigate, setErrorMessage }: authProps) {
    toggleLoad(true);

    // get session data from local storage
    const userName: string = window.localStorage.getItem('username') || '';
    const token: string = window.localStorage.getItem('sessionToken') || '';


    RequestHandler.POST('check-session', { 'username': userName, 'token': token }).then(
        (response) => {
            toggleLoad(false);

            if (response.success) {
                toggleLogIn(true);
            } else {
                if (response.message === 'Profile Error') {
                    navigate('/profile');
                } else {
                    setErrorMessage(response.message);
                }
            }
        }
    )
}

export default authenticate