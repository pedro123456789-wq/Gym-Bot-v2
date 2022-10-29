import { useEffect, useState } from "react";
import RequestHandler from "../RequestHandler/RequestHandler";
import LoadingPage from "../LoadingPage/LoadingPage";
import ProfileCreationPage from "./ProfileCreationPage";

function ProfileCreation() {
    const [isValid, setValid] = useState(false);
    const [isLoading, setLoad] = useState(true);


    function hasProfile() {
        const userName = localStorage.getItem('username');
        const sessionToken = localStorage.getItem('sessionToken');

        RequestHandler.GET('check-session', {
            username: userName,
            token: sessionToken
        }).then(response => {
            console.log(response.success);
            if (!response.success){
                console.log(response.message);
                if (response.message === 'Profile Error'){
                    setValid(true);
                }
            }
            
            setLoad(false);
        })
    }


    useEffect(hasProfile, [])


    return (
        isLoading ? <LoadingPage backgroundColor='white' />
            : isValid ? <ProfileCreationPage /> :
                <h1 className = 'text-center mt-5 pt-5'>Page not found</h1>
    );
}

export default ProfileCreation;