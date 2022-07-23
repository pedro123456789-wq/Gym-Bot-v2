import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import {
    AddCircleOutlined
} from '@material-ui/icons';

import { useState } from "react";

import RequestHandler from "../RequestHandler/RequestHandler";
import useStyles from './styles';
import { menuProps } from './Workouts';
import { alertType, defaultAlertState, CustomAlert } from '../CustomAlert/CustomAlert';




interface exercise {
    exerciseName: string | null,
    exerciseRepetitions: number | null,
    hours: number | null,
    minutes: number | null,
    seconds: number | null
}


const defaultValues: exercise = {
    exerciseName: null,
    exerciseRepetitions: null,
    hours: null,
    minutes: null,
    seconds: null
}



function AddWorkout({ toggleMode }: menuProps) {
    const classes = useStyles();

    const [workoutName, setWorkoutName] = useState<string>('');
    const [caloriesBurned, setCaloriesBurned] = useState<number | null>(null);

    const [exerciseList, modifyList] = useState<exercise[]>();
    const [exerciseValues, setExerciseValues] = useState<exercise>(defaultValues);
    const [showExerciseInput, toggleExerciseInput] = useState<boolean>(false);

    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);


    const handleInputChange = (e: any) => {
        let { name, value } = e.target;

        if (value === '') {
            value = null;
        }

        if (name !== 'exerciseName') {
            value = parseInt(value);
        }


        setExerciseValues({
            ...exerciseValues,
            [name]: value,
        });
    }

    function saveWorkout() {
        // check if workout name was entered 
        if (workoutName === '') {
            setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter a workout name' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            return -1;
        }
        
        //@ts-ignore 'Object is possibly null'
        if (isNaN(caloriesBurned) || setCaloriesBurned === null || caloriesBurned < 1) {
            setAlertState({ isShow: true, isSuccess: false, message: 'Invalid value entered for calories burned' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            return -1;
        }

        // check if at least one exercise was added
        if (exerciseList === null || exerciseList === undefined) {
            setAlertState({ isShow: true, isSuccess: false, message: 'You did not add any exercises' });
            setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
            setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            return -1;
        } else {
            //@ts-ignore: Object is possibly 'null'.
            if (exerciseList.length < 1) {
                setAlertState({ isShow: true, isSuccess: false, message: 'You did not add any exercises' })
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
                return -1;
            }
        }

        let addedExercises: { name: string | null; repetitions: number | null; durationSeconds: number | null; }[] = [];

        // @ts-ignore: Object is possibly 'null'.
        exerciseList.forEach((exercise) => {
            // add exercises to list 
            addedExercises.push({
                name: exercise.exerciseName,
                repetitions: exercise.exerciseRepetitions,
                durationSeconds: ((exercise.hours ?? 0) * 3600) + ((exercise.minutes ?? 0) * 60) + (exercise.seconds ?? 0)
            });
        });


        // send request to server to create new workout
        RequestHandler.POST('workouts', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken'),
            name: workoutName,
            caloriesBurned: caloriesBurned, 
            exercises: addedExercises
        }).then((response) => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Workout saved' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    //Go back to workouts menu   
                    toggleMode('menu')
                }, 2000);


            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }
        })


        // create workout 

    }


    function addExercise() {
        for (const value of Object.values(exerciseValues)) {
            if (value === null || value === '') {
                setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter a value for some fields' });

                // move window down to ensure user sees alert
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
                return -1;
            }
        }

        let newExercise: exercise = {
            exerciseName: exerciseValues.exerciseName,
            exerciseRepetitions: exerciseValues.exerciseRepetitions,
            hours: exerciseValues.hours,
            minutes: exerciseValues.minutes,
            seconds: exerciseValues.seconds,
        }

        setExerciseValues(defaultValues);

        modifyList([...exerciseList ?? [], newExercise]);
        setAlertState({ isShow: true, isSuccess: true, message: 'Added exercise' });
        toggleExerciseInput(false);

        // move window down to ensure user sees alert
        setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 500)
        setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);

        return 1;
    }

    return (
        <div className={classes.content}>
            <h3 className='text-center pb-5'>
                Add Workout
            </h3>

            <CustomAlert alertState={alertState} />

            <Grid container alignItems='center' justify='center' direction='column'>
                <Grid item>
                    <TextField
                        id='workout-name'
                        name='workout-name'
                        label='Workout Name'
                        type='text'
                        value={workoutName}
                        onChange={(e) => setWorkoutName(e.target.value)}
                        margin='normal'
                        fullWidth
                    />
                </Grid>

                <Grid item>
                    <TextField
                        id='calories-burned'
                        name='calories-burned'
                        label='Calories Burned'
                        type='number'
                        value={caloriesBurned}
                        onChange={(e) => setCaloriesBurned(parseInt(e.target.value))}
                        margin='normal'
                        fullWidth
                    />
                </Grid>

                <div className='mt-5'>
                    <Grid container alignItems='center' justify='center' direction='column'>
                        {
                            exerciseList?.map((exercise) => {
                                return (
                                    <Grid item>
                                        <div className={classes.exerciseDiv}>
                                            <h5>{exercise.exerciseName}</h5>
                                            <p className='mt-4'>Repetitions: {exercise.exerciseRepetitions}</p>
                                            <p>Duration: {("0" + exercise.hours).slice(-2)} : {("0" + exercise.minutes).slice(-2)} : {("0" + exercise.seconds).slice(-2)}</p>
                                        </div>
                                    </Grid>
                                )
                            })
                        }

                    </Grid>
                </div>

                <Grid item>
                    <button className={classes.addExerciseButton} onClick={() => toggleExerciseInput(!showExerciseInput)}>
                        <AddCircleOutlined style={{ fontSize: '300%' }} />
                        Add Exercise
                    </button>
                </Grid>
            </Grid>

            {showExerciseInput &&
                <Grid container alignItems='center' justify='center' direction='column'>
                    <Grid item>
                        <TextField
                            id='exerciseName'
                            name='exerciseName'
                            label='Exercise Name'
                            type='text'
                            value={exerciseValues.exerciseName}
                            onChange={handleInputChange}
                            margin='normal'
                            fullWidth
                        />
                    </Grid>

                    <Grid item>
                        <TextField
                            id='exerciseRepetitions'
                            name='exerciseRepetitions'
                            label='Exercise Repetitions'
                            type='number'
                            value={exerciseValues.exerciseRepetitions}
                            onChange={handleInputChange}
                            margin='normal'
                            fullWidth
                        />
                    </Grid>


                    <Grid item>
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
                    </Grid>

                    <Grid item>
                        <button className={classes.actionButton}
                            style={{ background: '#022669', color: 'white' }}
                            onClick={addExercise}>
                            Add Exercise
                        </button>
                    </Grid>
                </Grid>
            }

            <Grid container alignItems='center' justify='center' direction='column'>
                <Grid item>
                    <button className={classes.actionButton}
                        style={{ background: 'gray', color: 'white' }}
                        onClick={() => saveWorkout()}>
                        Save Workout
                    </button>
                </Grid>
            </Grid>
        </div>
    );
}

export default AddWorkout;