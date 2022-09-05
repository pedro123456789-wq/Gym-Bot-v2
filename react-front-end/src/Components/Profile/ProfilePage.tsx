import { Grid, TextField } from "@material-ui/core";
import { useTheme } from "@material-ui/styles";
import { useEffect, useState } from "react";
import { cammelCaseToText } from "../GlobalVariables";
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import RequestHandler from "../RequestHandler/RequestHandler";
import { Adb, DoneSharp, EditSharp } from '@material-ui/icons';
import { alertType, defaultAlertState, CustomAlert } from '../CustomAlert/CustomAlert';

import SideBar from "../SideBar/SideBar";
import useStyles from './styles';


interface profile {
    height: number | null,
    weight: number | null,
    vo2Max: number | null,
    age: number | null,
    gender: string | number,
}


let defaultProfileValues: profile = {
    height: null,
    weight: null,
    vo2Max: null,
    age: null,
    gender: ''
}

function ProfilePage() {
    const classes = useStyles();
    const theme = useTheme();
    const [profileValues, setProfileValues] = useState<profile>(defaultProfileValues);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [isLoading, toggleLoad] = useState<boolean>(true);
    const [canEdit, toggleEdit] = useState<boolean>(false);

    function handleInputChange(e: any) {
        let { name, value } = e.target;
        setProfileValues({ ...profileValues, [name]: parseInt(value) });
    }


    function fetchProfileValues() {
        toggleLoad(true);

        RequestHandler.GET('profile', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken')
        }).then(response => {
            if (response.success) {
                const data = response.data;
                const profileData: profile = {
                    height: data.height,
                    weight: data.weight,
                    vo2Max: data.vo2Max,
                    gender: data.gender == 1 ? 'Male' : 'Female',
                    age: data.age
                }

                setProfileValues(profileData);
                defaultProfileValues = profileData;
            } else {
                return -1;
            }

            toggleLoad(false);
        });
    }


    function saveChanges() {
        const inputValues = Object.values(profileValues);

        // check if any changes were made
        // do not send request if no changes were made to save server resources
        if (Object.values(inputValues).sort().toString() === Object.values(defaultProfileValues).sort().toString()){
            toggleEdit(false);
            return -1;
        }

        if (inputValues.includes('') || inputValues.includes(null) || inputValues.includes(undefined)) {
            setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter some values' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            return -1;
        }

        toggleLoad(true);
        let gender = profileValues.gender == 'Male' ? 1 : 0;
        profileValues.gender = gender;

        RequestHandler.PUT('profile', {
            ...profileValues, 
            username: window.localStorage.getItem('username'), 
            token: window.localStorage.getItem('sessionToken')
        }).then(response => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Changes saved' });
                toggleEdit(false);
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 1500);
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }

            toggleLoad(false);
        })
    }

    useEffect(fetchProfileValues, [])


    return (
        <div>
            <SideBar />
            <CustomAlert alertState={alertState} />

            <div className={classes.content}>
                <Grid container justify='center' direction='row' style={{ background: '#06064a', padding: '1.5rem' }} spacing={5}>
                    <Grid item className = 'pt-3'>
                        <Adb className={classes.adminIcon} />
                    </Grid>

                    <Grid item className = 'pt-4'>
                        <h3 className='text-center' style={{ color: 'white' }}>
                            {window.localStorage.getItem('username')}
                        </h3>
                    </Grid>
                </Grid>

                <div className='text-center mt-5'>
                    {isLoading &&
                        <LoadingIndicator />
                    }
                </div>

                {!isLoading &&
                    <Grid container justify='center' alignItems='center' direction='column'>
                        {
                            Object.entries(profileValues).map(([key, value]) => {
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
                                            disabled={key === 'gender' ? true : !canEdit}
                                            className={classes.disabledInput}
                                            fullWidth
                                        />
                                    </Grid>
                                );
                            })
                        }

                        <Grid item>
                            {canEdit ?
                                <button className={classes.actionButton} style={{ color: 'green' }} onClick={() => saveChanges()}>
                                    <DoneSharp className={classes.actionIcon} />
                                </button>
                                :
                                <button className={classes.actionButton} onClick={() => toggleEdit(!canEdit)}>
                                    <EditSharp className={classes.actionIcon} />
                                </button>
                            }
                        </Grid>
                    </Grid>
                }
            </div>
        </div>
    );
}

export default ProfilePage;