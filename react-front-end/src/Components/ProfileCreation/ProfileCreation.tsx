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

        RequestHandler.POST('has-profile', {
            username: userName,
            token: sessionToken
        }).then(response => {
            if (response.success) {
                setValid(true);
            }

            setLoad(false);
        })
    }


    useEffect(hasProfile, [])


    return (
        isLoading ? <LoadingPage backgroundColor='white' />
            : isValid ? <ProfileCreationPage /> :
                <h1>You already have a profile</h1>
    );
}

export default ProfileCreation;