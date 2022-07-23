import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';

import { useState } from 'react';

import RequestHandler from '../RequestHandler/RequestHandler';
import useStyles from './styles';
import { menuProps } from './Workouts';
import { alertType, defaultAlertState, CustomAlert } from '../CustomAlert/CustomAlert'



// TODO:
// Add back button
// Use alert state

interface run {
    distance: number | null,
    caloriesBurned: number | null,
    hours: number | null,
    minutes: number | null,
    seconds: number | null
}


const defaultValues: run = {
    distance: null,
    caloriesBurned: null,
    hours: null,
    minutes: null,
    seconds: null
};


function AddRunPage({ toggleMode }: menuProps) {
    const classes = useStyles();
    const [formValues, setFormValues] = useState<run>(defaultValues);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);

    const handleInputChange = (e: any) => {
        let { name, value } = e.target;
        value = parseInt(value);

        setFormValues({
            ...formValues,
            [name]: value,
        });
    }

    const handleSubmit = (e: any) => {
        e.preventDefault();
        console.log(formValues);

        // check for empty fields
        for (const value of Object.values(formValues)) {
            if (value === null || isNaN(value)) {
                setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter some values' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
                return -1;
            }
        }

        // send request to server
        // @ts-ignore: Object is possibly 'null'.
        const durationSeconds = (formValues.hours * 3600) + (formValues.minutes * 60) + formValues.seconds;
        RequestHandler.POST('runs', {
            'username': localStorage.getItem('username'),
            'token': localStorage.getItem('sessionToken'),
            'distance': formValues.distance,
            'caloriesBurned': formValues.caloriesBurned,
            'durationSeconds': durationSeconds
        }
        ).then(response => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Your run has been saved' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    toggleMode('menu');
                }, 2000);
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }
        });
    };

    return (
        <div className={classes.content}>
            <div>
                <h3 className='text-center pb-5'>
                    Add Run
                </h3>

                <div className='mt-3'>
                    <CustomAlert alertState={alertState} />
                </div>

                <form onSubmit={handleSubmit}>
                    <Grid container alignItems='center' justify='center' direction='column' spacing={5}>
                        <Grid item>
                            <TextField
                                id='distance-ran'
                                name='distance'
                                label='Distance Ran'
                                type='number'
                                value={formValues.distance}
                                onChange={handleInputChange}
                                margin='normal'
                                fullWidth
                            />
                        </Grid>

                        <Grid item>
                            <TextField
                                id='calories-burned'
                                name='caloriesBurned'
                                label='Calories Burned'
                                type='number'
                                value={formValues.caloriesBurned}
                                onChange={handleInputChange}
                                margin='normal'
                                fullWidth
                            />
                        </Grid>

                        <Grid item>
                            <p className={classes.inputLabel}>Time</p>

                            <input type='number'
                                style={{ 'maxWidth': '2rem' }}
                                min={0}
                                max={999}
                                placeholder='H'
                                name='hours'
                                onChange={handleInputChange}>
                            </input>
                            <label className='ml-2 mr-2'>:</label>

                            <input type='number'
                                style={{ 'maxWidth': '2rem' }}
                                min={0}
                                max={60}
                                placeholder='M'
                                name='minutes'
                                onChange={handleInputChange}>
                            </input>
                            <label className='ml-2 mr-2'>:</label>

                            <input type='number'
                                style={{ 'maxWidth': '2rem' }}
                                min={0}
                                max={60}
                                placeholder='S'
                                name='seconds'
                                onChange={handleInputChange}>
                            </input>
                        </Grid>

                        <Grid item>
                            <input className={classes.actionButton}
                                style={{ background: '#022669', color: 'white' }}
                                type='submit'
                                value='Save Run'>
                            </input>
                        </Grid>
                    </Grid>
                </form>
            </div>
        </div>
    );
}

export default AddRunPage;