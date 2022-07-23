import { duration, Grid } from '@material-ui/core';
import {
    PlayArrow,
    StopOutlined,
    ExitToApp
} from '@material-ui/icons';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { alertType, CustomAlert, defaultAlertState } from '../CustomAlert/CustomAlert';
import RequestHandler from '../RequestHandler/RequestHandler';
import useStyles from './styles';

// TODO: 
// Add calorie tracking options
// Show pop up when workout is saved

interface WorkoutState {
    hasStarted: boolean,
    isRunning: boolean,
    hasFinished: boolean,
    setNumber: number
}


const defaultWorkoutState: WorkoutState = {
    hasStarted: false,
    isRunning: false,
    hasFinished: false,
    setNumber: 0
}


interface DurationState {
    totalDurationSeconds: number,
    exerciseDurationSeconds: number,
    previousRunningState: boolean
}


const defaultDurationState: DurationState = {
    totalDurationSeconds: 0,
    exerciseDurationSeconds: 0,
    previousRunningState: true
}


interface Exercise {
    durationSeconds: number,
    name: string
}


function LiveWorkoutPage() {
    const classes = useStyles();
    //split into two different states because updating same state from two different functions causes problems
    const [workoutState, setWorkoutState] = useState<WorkoutState>(defaultWorkoutState);
    const [durationState, setDurationState] = useState<DurationState>(defaultDurationState);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const navigate = useNavigate();

    // used to avoid inconsistencies due to delay in time update
    const [isTimeVisible, setVisibility] = useState(true);

    // initialise with default element, since ts does not allow one to initialize with empty list 
    const [completedExercises, setCompletedExercises] = useState<[Exercise]>([{ durationSeconds: 0, name: '' }]);


    function saveWorkout() {
        // list to send exercises to server
        let addedExercises: { name: string | null; repetitions: number | null; durationSeconds: number | null; }[] = [];

        completedExercises.forEach((exercise) => {
            if (exercise.name !== "") {
                addedExercises.push({
                    name: exercise.name,
                    repetitions: 0,
                    durationSeconds: exercise.durationSeconds
                });
            }
        });

        console.log(completedExercises);

        RequestHandler.POST('workouts', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken'),
            name: 'Live Workout Session',
            caloriesBurned: 100,
            exercises: addedExercises
        }).then((response) => {
            if (response.success) {
                setAlertState({
                    isShow: true,
                    isSuccess: true,
                    message: 'Workout Saved successfuly'
                });
                navigate('/dashboard');
            } else {
                setAlertState({
                    isShow: true,
                    isSuccess: false,
                    message: response.message
                });
            }
        });
    }

    function addExercise() {
        let exercise: Exercise = {
            durationSeconds: durationState.exerciseDurationSeconds,
            name: `Exercise: ${workoutState.setNumber}`
        }

        var newList = completedExercises;
        newList.push(exercise);
        setCompletedExercises(newList);

        console.log(completedExercises);
    }


    function updateTime() {
        if (workoutState.hasStarted) {
            if (durationState.previousRunningState !== workoutState.isRunning) {
                setDurationState({
                    totalDurationSeconds: durationState.totalDurationSeconds + 1,
                    exerciseDurationSeconds: 0,
                    previousRunningState: workoutState.isRunning
                });

                setVisibility(true);
            } else {
                setDurationState({
                    totalDurationSeconds: durationState.totalDurationSeconds + 1,
                    exerciseDurationSeconds: durationState.exerciseDurationSeconds + 1,
                    previousRunningState: workoutState.isRunning
                });
            }
        }
    }

    function secondsToString(durationSeconds: number) {
        const minutes = Math.floor(durationSeconds / 60);
        const seconds = durationSeconds - (minutes * 60);

        let minutesString = minutes.toString();
        let secondsString = seconds.toString();

        if (minutes < 10) {
            minutesString = '0' + minutesString;
        }

        if (seconds < 10) {
            secondsString = '0' + secondsString;
        }

        return minutesString + ':' + secondsString
    }

    useEffect(() => {
        setTimeout(updateTime, 1000);
    })


    return (
        <div>
            <CustomAlert alertState={alertState} />

            <div className={classes.content} style={{ 'marginTop': '15vh' }}>
                <h3 className='text-center'>
                    {workoutState.hasStarted ? secondsToString(durationState.totalDurationSeconds)
                        : workoutState.hasFinished ? 'Workout Completed'
                            : 'Press button to start workout'}
                </h3>

                {workoutState.hasStarted &&
                    <div className='text-center'>
                        <h4 className='mt-5'>
                            {workoutState.isRunning ? `Set: ${workoutState.setNumber.toString()}` : 'Rest'}
                        </h4>

                        {isTimeVisible &&
                            <h5>
                                {secondsToString(durationState.exerciseDurationSeconds)}
                            </h5>
                        }
                    </div>
                }

                <div style={{ 'marginTop': '15vh' }}>
                    {!workoutState.hasFinished ?
                        <Grid container spacing={2} className={classes.gridRoot}>
                            {(workoutState.hasStarted === false || workoutState.isRunning === false) &&
                                <Grid item xs={12} sm={12} md={12}>
                                    <div className={classes.optionDiv} style={{ background: 'transparent' }}>
                                        <button className={classes.workoutButton}
                                            onClick={() => {
                                                setWorkoutState({
                                                    ...workoutState,
                                                    isRunning: true,
                                                    hasStarted: true,
                                                    setNumber: workoutState.setNumber + 1
                                                });
                                            }}
                                        >
                                            <PlayArrow style={{ fontSize: '3rem', color: '#06064a' }} />
                                        </button>
                                    </div>
                                </Grid>
                            }

                            {(workoutState.hasStarted === true) ?
                                (workoutState.isRunning === true) ?
                                    <Grid item xs={12} sm={12} md={12} alignItems='center'>
                                        <div className={classes.optionDiv} style={{ background: 'transparent' }}>
                                            <button className={classes.workoutButton}
                                                onClick={() => {
                                                    setWorkoutState({
                                                        ...workoutState,
                                                        isRunning: false
                                                    });

                                                    setVisibility(false);
                                                    addExercise();
                                                }}
                                            >
                                                <StopOutlined style={{ fontSize: '3rem', color: '#06064a' }} />
                                            </button>
                                        </div>
                                    </Grid>
                                    :
                                    <Grid item xs={12} sm={12} md={12}>
                                        <div className={classes.optionDiv} style={{ background: 'transparent' }}>
                                            <button className={classes.workoutButton}
                                                onClick={() =>
                                                    setWorkoutState({
                                                        ...workoutState,
                                                        isRunning: false,
                                                        hasStarted: false,
                                                        hasFinished: true
                                                    })
                                                }>
                                                <ExitToApp style={{ fontSize: '2rem', color: 'black' }} />
                                            </button>
                                        </div>
                                    </Grid>
                                : ''}
                        </Grid>
                        : <>
                            <Grid container spacing={5} className={classes.gridRoot} alignItems='center' direction='column'>
                                <Grid item xs={12} md={6} sm={12}>
                                    <div className='text-center'>
                                        <div>
                                            <h5>Exercises: {workoutState.setNumber}</h5>
                                        </div>

                                        <div className='mt-3'>
                                            <h5>Workout Duration: {secondsToString(durationState.totalDurationSeconds)}</h5>
                                        </div>

                                        <div className = 'mt-4'>
                                            <input placeholder = 'Calories Burned' type = 'number' className = 'mr-1'/>
                                            <button className = {classes.smallButton}>Calculate</button>
                                        </div>
                                    </div>
                                </Grid>

                                <Grid item xs={12} md={6} sm={12}>
                                    <div className='text-center'>
                                        <div>
                                            <button className={classes.actionButton} style={{ background: 'gray' }} onClick={saveWorkout}>
                                                Save Workout
                                            </button>
                                        </div>

                                        <div className='mt-1'>
                                            <button className={classes.actionButton} style={{ margin: 0, background: 'gray' }}
                                                onClick={() => window.location.reload()}>
                                                Discard Workout
                                            </button>
                                        </div>
                                    </div>
                                </Grid>
                            </Grid>
                        </>
                    }
                </div>
            </div>
        </div>
    );
}


export default LiveWorkoutPage;