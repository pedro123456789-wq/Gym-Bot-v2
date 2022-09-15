import {
    Grid
} from '@material-ui/core';
import {
    DirectionsRun,
    FitnessCenter
} from '@material-ui/icons';

import { useEffect, useState } from 'react';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
import RequestHandler from '../RequestHandler/RequestHandler';
import useStyles from './styles';
import { menuProps } from './Workouts';



function WorkoutMenu({ toggleMode }: menuProps) {
    const classes = useStyles();
    const [distanceRan, setDistanceRan] = useState<number>(-1);
    const [vo2Max, setVo2Max] = useState<number>(-1);
    const [workoutNumber, setWorkoutNumber] = useState<number>(-1);
    const [caloriesBurned, setCaloriesBurned] = useState<number>(-1);


    function dateToString(date: Date) {
        var dd = String(date.getDate()).padStart(2, '0');
        var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0
        var yyyy = date.getFullYear();
        return `${dd}/${mm}/${yyyy}`;
    }

    // fetch data from last 7 days
    function fetchData() {
        var endDateObj = new Date();
        endDateObj.setDate(endDateObj.getDate() + 1); // server query is non-inclusive so end date needs to be one more than final date
        const interval = 7;
        var startDateObj = new Date();
        startDateObj.setDate(startDateObj.getDate() - interval);

        var startDate = dateToString(startDateObj);
        var endDate = dateToString(endDateObj);

        // get run data
        RequestHandler.GET('runs', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken'),
            startDate: startDate,
            endDate: endDate
        }).then((response) => {
            if (response.success) {
                const runs = response.data.runs;
                var totalDistance = 0;

                for (let i = 0; i < runs.length; i++) {
                    const run = runs[i];
                    totalDistance += run.distance;
                }

                setDistanceRan(totalDistance);
            } else {
                console.log(response.message);
            }
        });

        // get vo2 max from profile data
        RequestHandler.GET('profile', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken')
        }).then((response) => {
            if (response.success) {
                setVo2Max(response.data.vo2Max);
            } else {
                console.log(response.message);
            }
        });

        //get workout data 
        RequestHandler.GET('workouts', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken'),
            startDate: startDate,
            endDate: endDate,
            targetWorkouts: 'ALL'
        }).then((response) => {
            if (response.success) {
                const workouts = response.workouts;
                setWorkoutNumber(workouts.length);

                var totalCalories = 0;
                workouts.forEach((workout: any) => totalCalories += workout.caloriesBurned);
                setCaloriesBurned(totalCalories);
            } else {
                console.log(response.message);
            }
        })
    }

    useEffect(fetchData, []);

    return (
        <div className={classes.content}>
            <Grid container spacing={2} className={classes.gridRoot}>
                <Grid item xs={12} sm={12} md={6}>
                    <div className={classes.optionDiv}>
                        <h4>Running</h4>

                        <div>
                            <DirectionsRun className={classes.optionIcon} />
                        </div>

                        {(distanceRan === -1 || vo2Max === -1) ?
                            <div className='text-center' style = {{maxHeight: '10vh'}}>
                                <LoadingIndicator />
                            </div>
                            :
                            <div>
                                <h5 className='text-center mt-4 mb-4'>Last 7 days</h5>
                                <p className={classes.smallText}>Distance Ran: {distanceRan}</p>
                                <p className={classes.smallText}>Vo2 Max: {vo2Max}</p>
                            </div>
                        }

                        {/* change page to running section */}
                        <button className={classes.actionButton} onClick={() => toggleMode('run')}>
                            Add Run
                        </button>
                    </div>
                </Grid>

                <Grid item xs={12} sm={12} md={6}>
                    <div className={classes.optionDiv}>
                        <h4>Strength training</h4>

                        <div>
                            <FitnessCenter className={classes.optionIcon} />
                        </div>

                        {(workoutNumber === -1 || caloriesBurned === -1) ?
                            <div className='text-center' style = {{maxHeight: '10vh'}}>
                                <LoadingIndicator />
                            </div>
                            :
                            <>
                                <h5 className='text-center mt-4 mb-4'>Last 7 days: </h5>
                                <p className={classes.smallText}>Workouts Done: {workoutNumber}</p>
                                <p className={classes.smallText}>Calories Burned: {caloriesBurned}</p>
                            </>
                        }


                        <button className={classes.actionButton} onClick={() => toggleMode('liveWorkout')}>
                            Start  Workout
                        </button>

                        <button className={classes.actionButton} onClick={() => toggleMode('addWorkout')}>
                            Add workout
                        </button>
                    </div>
                </Grid>
            </Grid>
        </div>
    );
}

export default WorkoutMenu;