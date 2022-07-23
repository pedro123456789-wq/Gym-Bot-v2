import { useState } from 'react';
import Navbar from '../NavBar/Navbar';
import RequestHandler from '../RequestHandler/RequestHandler';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
import { useNavigate } from 'react-router-dom';
import { CustomAlert, alertType, defaultAlertState } from '../CustomAlert/CustomAlert';
import { Grid, TextField } from '@material-ui/core';
import useStyles from './styles';


function EmailConfirmationPage() {
    const [confirmationCode, setConfirmationCode] = useState<number | null>(null);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const classes = useStyles();
    const navigate = useNavigate();


    function confirmEmail(e: any) {
        e.preventDefault();
        toggleLoad(true);

        if (confirmationCode == null || isNaN(confirmationCode)) {
            setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter a confirmation code' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
        }

        // get username from local storage 
        const userName: string = window.localStorage.getItem('username') || '';

        RequestHandler.PUT('confirm-email', {
            'username': userName,
            'confirmationCode': confirmationCode
        }).then(
            (response) => {
                toggleLoad(false);

                if (response.success) {
                    setAlertState({ isShow: true, isSuccess: true, message: 'Email Verified' });
                    setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                    setTimeout(() => {
                        setAlertState({ ...alertState, isShow: false });
                        navigate('/log-in');
                    }, 1500)
                } else {
                    setAlertState({ isShow: true, isSuccess: false, message: response.message });
                    setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                    setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
                }
            }
        );
    }

    return (
        <div>
            <Navbar />

            <h3 className='text-center mt-5 pt-5'>
                Confirm Email
            </h3>


            <div>
                <CustomAlert alertState={alertState} />

                <div className='mt-5 pt-5'>
                    <form onSubmit = {confirmEmail}>
                        <Grid container justify='center' alignItems='center' direction='column' spacing={2}>
                            <Grid item>
                                <TextField
                                    id='confirmationCode'
                                    name='confirmationCode'
                                    label='Confirmation Code'
                                    type='text'
                                    value={confirmationCode}
                                    onChange={(e: any) => setConfirmationCode(e.target.value)}
                                    margin='normal'
                                    fullWidth
                                />
                            </Grid>

                            <Grid item>
                                <input type='submit' value='Confirm Email' className = {classes.actionButton}/>
                            </Grid>

                            <Grid item>
                                {isLoading && <LoadingIndicator />}
                            </Grid>
                        </Grid>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default EmailConfirmationPage;