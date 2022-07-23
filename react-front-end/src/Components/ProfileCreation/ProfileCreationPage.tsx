import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { cammelCaseToText } from "../GlobalVariables";
import Navbar from "../NavBar/Navbar";
import RequestHandler from "../RequestHandler/RequestHandler";

function ProfileCreationPage() {
    const [profileFields, setProfile] = useState({
        'height': null,
        'weight': null,
        'vo2Max': null,
        'age': null,
        'gender': null
    });

    const [targetFields, setTargets] = useState({
        'caloriesEatenTarget': null,
        'caloriesBurnedTarget': null,
        'minutesTrainedTarget': null,
        'distanceRanTarget': null,
    });

    const navigate = useNavigate();


    function createProfile() {
        // get login token and username from local storage 
        const userName = window.localStorage.getItem('username')
        const token = window.localStorage.getItem('sessionToken')

        if (userName === null || token === null) {
            alert('Session not valid');
            return;
        }

        // merge profile and targets dictionary
        const requestPayload = Object.assign({ username: userName, token: token }, profileFields, targetFields)
        console.log(requestPayload)


        RequestHandler.POST('profile', requestPayload)
            .then((response) => {
                alert(response.message)
                navigate('/dashboard')
            }
            )
    }


    return (
        <div className='text-center'>
            <Navbar />
            <h1 className='mt-3'>Profile</h1>


            <div className='mt-5'>
                <form>
                    {Object.keys(profileFields).map((field) => {
                        return (
                            // TODO: Add select section for gender
                            <div className='form-group'>
                                <label htmlFor={field}>{cammelCaseToText(field)}</label>

                                <div className='mt-4 mb-4'>
                                    <input type='number'
                                        id={field}
                                        className='form-control text-center'
                                        placeholder='Enter Username'
                                        style={{ width: '40vw', display: 'inline-block' }}
                                        onChange={event => setProfile(previousState => {
                                            return {
                                                ...previousState,
                                                [field]: parseFloat(event.target.value)
                                            }
                                        })}
                                    />
                                </div>
                            </div>
                        )
                    })}
                </form>
            </div>

            <h1 className='mt-5'>Targets</h1>
            <div className='mt-5'>
                <form>
                    {Object.keys(targetFields).map((field) => {
                        return (
                            // TODO: Add select section for gender
                            <div className='form-group'>
                                <label htmlFor={field}>{cammelCaseToText(field)}</label>

                                <div className='mt-4 mb-4'>
                                    <input type='number'
                                        id={field}
                                        className='form-control text-center'
                                        placeholder='Enter Username'
                                        style={{ width: '40vw', display: 'inline-block' }}
                                        onChange={event => setTargets(previousState => {
                                            return {
                                                ...previousState,
                                                [field]: parseFloat(event.target.value)
                                            }
                                        })}
                                    />
                                </div>
                            </div>
                        )
                    })}
                </form>
            </div>


            <button className='btn btn-dark btn-block text-center mt-5 pt-3 pb-3'
                style={{ fontSize: '1.3rem' }}
                onClick={createProfile}>
                Save Profile
            </button>

        </div>
    );
}

export default ProfileCreationPage;