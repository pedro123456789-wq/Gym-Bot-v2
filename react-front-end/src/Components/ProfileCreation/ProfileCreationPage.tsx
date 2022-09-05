import { FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, TextField } from "@material-ui/core";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { alertType, defaultAlertState, CustomAlert } from "../CustomAlert/CustomAlert";
import { cammelCaseToText } from "../GlobalVariables";
import Navbar from "../NavBar/Navbar";
import RequestHandler from "../RequestHandler/RequestHandler";
import useStyles from './styles';


interface profileType {
    height: number | null,
    weight: number | null,
    vo2Max: number | null,
    age: number | null,
    gender: number
}

const defaultProfileData: profileType = {
    height: null,
    weight: null,
    vo2Max: null,
    age: null,
    gender: -1
}


interface targetsType {
    caloriesEatenTarget: number | null,
    caloriesBurnedTarget: number | null,
    minutesTrainedTarget: number | null,
    distanceRanTarget: number | null
}

const defaultTargetData: targetsType = {
    caloriesEatenTarget: null,
    caloriesBurnedTarget: null,
    minutesTrainedTarget: null,
    distanceRanTarget: null
}


function ProfileCreationPage() {
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [profileData, setProfileData] = useState<profileType>(defaultProfileData);
    const [targetData, setTargetData] = useState<targetsType>(defaultTargetData);
    const navigate = useNavigate();
    const classes = useStyles();

    function createProfile() {
        // get login token and username from local storage 
        const userName = window.localStorage.getItem('username')
        const token = window.localStorage.getItem('sessionToken')

        if (userName === null || token === null) {
            window.scrollTo({ top: 0, behavior: 'smooth' })
            setAlertState({ isShow: true, isSuccess: false, message: 'Session is not valid' })
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
        }

        // merge profile and targets dictionary
        const requestPayload = Object.assign({ username: userName, token: token }, profileData, targetData)

        RequestHandler.POST('profile', requestPayload).then((response) => {
            if (response.success) {
                window.scrollTo({ top: 0, behavior: 'smooth' })
                setAlertState({ isShow: true, isSuccess: true, message: 'Profile Created' });
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    navigate('/dashboard');
                }, 2000)
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' })
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000)
            }
        })
    }


    function handleProfileInput(e: any) {
        const { name, value } = e.target;
        setProfileData({ ...profileData, [name]: parseInt(value)});
    }

    function handleTargetsInput(e: any) {
        const { name, value } = e.target;

        if (name == 'distanceRanTarget'){
            setTargetData({...targetData, [name]: parseFloat(value) * 1000});
        }else{
            setTargetData({ ...targetData, [name]: parseInt(value) });
        }
    }

    function handleRadioInput(e: any) {
        const { _, value } = e.target;
        var genderNumber;

        if (value === 'male') {
            genderNumber = 1;
        } else {
            genderNumber = 0
        }

        setProfileData({ ...profileData, gender: genderNumber })

    }


    return (
        <div>
            <Navbar />

            <h3 className='text-center mt-5 pt-5'>
                Profile
            </h3>

            <div>
                <CustomAlert alertState={alertState} />

                <div className='mt-3'>
                    <Grid container alignItems='center' justifyContent='center' direction='column' spacing={3}>
                        {/* Height */}
                        <Grid item>
                            <TextField
                                id='height'
                                name='height'
                                label='Height (cm)'
                                type={'number'}
                                onChange={handleProfileInput}
                                margin='normal'
                            />
                        </Grid>

                        {/* Weight */}
                        <Grid item>
                            <TextField
                                id='weight'
                                name='weight'
                                label='Weight (kg)'
                                type={'number'}
                                onChange={handleProfileInput}
                                margin='normal'
                            />
                        </Grid>

                        {/* Vo2 Max */}
                        <Grid item>
                            <TextField
                                id='vo2Max'
                                name='vo2Max'
                                label='Vo2 Max (ml/kg/min)'
                                type={'number'}
                                onChange={handleProfileInput}
                                margin='normal'
                            />
                        </Grid>

                        {/* Age*/}
                        <Grid item>
                            <TextField
                                id='age'
                                name='age'
                                label='Age'
                                type={'number'}
                                onChange={handleProfileInput}
                                margin='normal'
                            />
                        </Grid>

                        {/* Gender */}
                        <Grid item>
                            <RadioGroup name='gender' onChange={handleRadioInput} row>
                                <FormControlLabel value='male'
                                    control={<Radio classes={{ root: classes.radio, checked: classes.checked }} />}
                                    label='Male' />
                                <FormControlLabel value='female'
                                    control={<Radio classes={{ root: classes.radio, checked: classes.checked }} />}
                                    label='Female' />
                            </RadioGroup>
                        </Grid>
                    </Grid>
                </div>
            </div>

            <h3 className='mt-5 pt-3 text-center'>Targets</h3>
            <div className='mt-3'>
                <Grid container alignItems='center' justifyContent='center' direction='column' spacing={3}>
                    {/* Calories Eaten */}
                    <Grid item>
                        <TextField
                            id='caloriesEatenTarget'
                            name='caloriesEatenTarget'
                            label='Calories Eaten'
                            type={'number'}
                            onChange={handleTargetsInput}
                            margin='normal'
                        />
                    </Grid>

                    {/* Calories Burned */}
                    <Grid item>
                        <TextField
                            id='caloriesBurnedTarget'
                            name='caloriesBurnedTarget'
                            label='Calories Burned'
                            type={'number'}
                            onChange={handleTargetsInput}
                            margin='normal'
                        />
                    </Grid>

                    {/* Minutes Trained */}
                    <Grid item>
                        <TextField
                            id='minutesTrainedTarget'
                            name='minutesTrainedTarget'
                            label='Minutes Trained Target'
                            type={'number'}
                            onChange={handleTargetsInput}
                            margin='normal'
                        />
                    </Grid>

                    {/* Distance Ran*/}
                    <Grid item>
                        <TextField
                            id='distanceRanTarget'
                            name='distanceRanTarget'
                            label='Distance Ran Target (Km)'
                            type={'number'}
                            onChange={handleTargetsInput}
                            margin='normal'
                            inputProps={{
                                step: 0.01
                            }}
                        />
                    </Grid>
                </Grid>
            </div>

            <div className='mt-5 text-center pb-3'>
                <button className={classes.actionButton} onClick={createProfile}>
                    <h5 className='pl-5 pr-5 pt-3 pb-2'>Save Profile</h5>
                </button>
            </div>
        </div>
    );
}

export default ProfileCreationPage;