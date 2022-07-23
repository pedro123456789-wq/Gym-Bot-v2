import Navbar from "../NavBar/Navbar";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RequestHandler from "../RequestHandler/RequestHandler";
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import useStyles from './styles';
import { alertType, defaultAlertState, CustomAlert } from '../CustomAlert/CustomAlert';
import { Grid, TextField } from "@material-ui/core";
import { cammelCaseToText } from "../GlobalVariables";



interface userDetails {
    username: string,
    email: string,
    password: string,
    passwordConfirmation: string
}


const defaultValues: userDetails = {
    username: '',
    email: '',
    password: '',
    passwordConfirmation: ''
}


function SignUpPage() {
    // store user inputs
    const [userDetails, setUserDetails] = useState<userDetails>(defaultValues);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);

    // loading inidicator state
    const [isLoading, toggleLoad] = useState<boolean>(false);

    // react navigation
    const navigate = useNavigate();
    const classes = useStyles();


    function handleInputChange(e: any) {
        const { name, value } = e.target;
        setUserDetails({ ...userDetails, [name]: value });
    }


    function handleSubmit(e: any) {
        e.preventDefault();

        if (userDetails.password !== userDetails.passwordConfirmation) {
            setAlertState({ isShow: true, isSuccess: false, message: 'The two passwords do not match' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            return -1;
        }

        const inputValues = Object.values(userDetails);

        if (inputValues.includes('') || inputValues.includes(null) || inputValues.includes(undefined)) {
            setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter some values' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            return -1;
        }

        toggleLoad(true);

        RequestHandler.POST('sign-up', {
            username: userDetails.username,
            password: userDetails.password,
            email: userDetails.email
        }).then(response => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Created account successfully' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    window.localStorage.setItem('username', userDetails.username);
                    navigate('/confirm-email');
                }, 2000);
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }

            toggleLoad(false);
        })
    }






    return (
        <div>
            <Navbar />

            <h3 className='text-center mt-5'>
                Sign Up
            </h3>

            <div>
                <CustomAlert alertState={alertState} />

                <div className='mt-4'>
                    <form onSubmit={handleSubmit}>
                        <Grid container justify='center' alignItems='center' direction='column' spacing={2}>
                            {
                                Object.entries(userDetails).map(([key, value]) => {
                                    return (
                                        <Grid item>
                                            <TextField
                                                id={key}
                                                name={key}
                                                label={cammelCaseToText(key)}
                                                type={key.includes('password') ? 'password' : 'text'}
                                                value={value}
                                                onChange={handleInputChange}
                                                margin='normal'
                                                fullWidth
                                            />
                                        </Grid>
                                    )
                                })
                            }

                            <Grid item>
                                <input value='Sign Up' className={classes.actionButton} type='submit' />
                            </Grid>

                            <Grid item>
                                {isLoading &&
                                    <LoadingIndicator />
                                }
                            </Grid>
                        </Grid>

                    </form>

                </div>
            </div>

        </div>
    );
}

export default SignUpPage;