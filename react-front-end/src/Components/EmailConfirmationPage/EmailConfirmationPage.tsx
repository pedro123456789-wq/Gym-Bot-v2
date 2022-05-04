import {useState} from 'react';
import Navbar from '../NavBar/Navbar';
import RequestHandler from '../RequestHandler/RequestHandler';
import Alert, {alertProps} from '../Alert/Alert';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
import {useNavigate} from 'react-router-dom';


function EmailConfirmationPage() {
    const [confirmationCode, setConfirmationCode] = useState<number>(0);
    const [alertData, setAlert] = useState<alertProps>({message: '', isSuccess: false});
    const [showAlert, toggleAlert] = useState<boolean>(false);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    
    const navigate = useNavigate();


    function confirmEmail(){
        toggleLoad(true);

        // get username from local storage 
        const userName:string  = window.localStorage.getItem('username') || '';

        RequestHandler.sendRequest('PUT', 
                                   'confirm-email', 
                                   {'username' : userName, 
                                    'confirmationCode' : confirmationCode}
        ).then(
            (response) => {
                toggleLoad(false);
                toggleAlert(true);

                if (response.success){
                    setAlert({
                         message: 'Account verified', 
                        isSuccess: true
                        })
                }else{
                    setAlert({
                        message: response.message, 
                        isSuccess: false
                    })
                }
            }
        )


        // hide alert after 2 seconds 
        setTimeout(() => {
            toggleAlert(false);
            navigate('/log-in');
        }, 2000)

    }
    
    return (
        <div>
            <Navbar />

            {
                <div className = 'mt-2'>
                    {showAlert && <Alert message = {alertData.message} isSuccess = {alertData.isSuccess}/>}
                </div>
            }

            <h1 className = 'text-center display-4 mt-5'>
                Confirm Email
            </h1>


            <form>
                <div className = 'form-group text-center mt-5 pt-5'>
                    <label htmlFor = 'email-confirmation' className = 'text-center'>Confirmation Code</label>

                    <div className = 'mt-5 mb-5 pb-5'>
                        <input type = 'number'
                               id = 'email-cofirmation'
                               className = 'form-control text-center'
                               placeholder = 'Enter Confirmation Code'
                               onChange = {event => setConfirmationCode(event.target.value as unknown as number)}
                        />
                    </div>

                    <div>
                        <button type = 'button' 
                            className = 'btn btn-dark btn-lg mt-3' 
                            style = {{width: '50vw'}}
                            onClick = {confirmEmail}>
                                Confirm Email
                        </button>
                    </div>
                </div>
            </form>

            {isLoading && <LoadingIndicator />}
        </div>
    );
}

export default EmailConfirmationPage;