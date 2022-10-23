import Navbar from "../NavBar/Navbar";
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RequestHandler from "../RequestHandler/RequestHandler";
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import { alertType, defaultAlertState, CustomAlert } from '../CustomAlert/CustomAlert';
import { Grid, TextField } from "@material-ui/core";
import { cammelCaseToText } from "../GlobalVariables";
import useStyles from './styles';




interface loginDetails {
    username: string | null,
    password: string | null
}


const defaultValues: loginDetails = {
    username: '',
    password: ''
}


function LoginPage() {
    const classes = useStyles();
    const [loginData, setLoginData] = useState<loginDetails>(defaultValues);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [isLoading, toggleLoad] = useState<boolean>(false);
    const navigate = useNavigate();

    function handleInputChange(e: any) {
        const { name, value } = e.target;
        setLoginData({ ...loginData, [name]: value });
    }


    function handleSubmit(e: any) {
        e.preventDefault();

        if (Object.values(loginData).includes('') || Object.values(loginData).includes(null) || Object.values(loginData).includes(undefined)) {
            setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter some values' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);

            return -1;
        }

        // show loading indicator
        toggleLoad(true);

        RequestHandler.POST('log-in', loginData).then(response => {
            if (response.success) {
                // save session token in local storage
                const token = response.token
                window.localStorage.setItem('sessionToken', token);
                window.localStorage.setItem('username', loginData.username || '');

                setAlertState({ isShow: true, isSuccess: true, message: 'Logged In successfully' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    navigate('/dashboard');
                }, 1500);
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

            <h3 className='text-center mt-5 pt-5'>
                Log In
            </h3>

            <div>
                <CustomAlert alertState={alertState} />

                <div className='mt-5 pt-5'>
                    <form onSubmit={handleSubmit}>
                        <Grid container alignItems='center' justify='center' direction='column' spacing={3}>
                            {Object.entries(loginData).map(([key, value]) => {
                                return (
                                    <Grid item>
                                        <TextField
                                            id={key}
                                            name={key}
                                            label={cammelCaseToText(key)}
                                            type={key == 'password' ? 'password' : 'text'}
                                            value={value}
                                            onChange={handleInputChange}
                                            margin='normal'
                                            fullWidth
                                        />
                                    </Grid>
                                )
                            })}

                            <Grid item>
                                <input className={classes.actionButton} value='Log In' type='submit' />
                            </Grid>

                            {isLoading &&
                                <Grid item>
                                    <LoadingIndicator />
                                </Grid>
                            }
                        </Grid>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default LoginPage;