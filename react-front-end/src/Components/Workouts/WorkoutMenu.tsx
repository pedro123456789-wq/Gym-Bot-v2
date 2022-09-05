import {
    Grid
} from '@material-ui/core';
import {
    DirectionsRun,
    FitnessCenter
} from '@material-ui/icons';

import { useState } from 'react';
import RequestHandler from '../RequestHandler/RequestHandler';
import useStyles from './styles';
import { menuProps } from './Workouts';


interface workoutData{
    distanceRan: number,
    vo2Max: number, 
    workoutNumber: number, 
    averageDuration: number 
}

const defaultWorkoutData: workoutData = {
    distanceRan: -1, 
    vo2Max: -1, 
    workoutNumber: -1, 
    averageDuration: -1
}


function WorkoutMenu({ toggleMode }: menuProps) {
    const classes = useStyles();
    const [workoutData, setWorkoutData] = useState<workoutData>(defaultWorkoutData);
    
    // fetch data from last 7 days
    function fetchData(){
        // get run data
        RequestHandler.GET('/runs', {
            username: window.localStorage.getItem('username'), 
            token: window.localStorage.getItem('sessionToken'), 
            startDate: 'ALL', 
            endDate: 'ALL'
        }).then((response) => {
            if (response.success){
                setWorkoutData({...workoutData, distanceRan: response.data.distance});
            }else{
                alert(response.message);
            }
        });

        RequestHandler.GET('/profile', {
            username: window.localStorage.getItem('username'), 
            token: window.localStorage.getItem('sessionToken')
        }).then((response) => {
            if (response.success){
                setWorkoutData({...workoutData, vo2Max: response.vo2Max});
            }
        });

        RequestHandler.GET('/workouts', {
            username: window.localStorage.getItem('username'), 
            token: window.localStorage.getItem('sessionToken'), 
            startingDate: '01/01/2000', 
            endDate: '01/01/2000', 
        })

    }

    return (
        <div className={classes.content}>
            <Grid container spacing={2} className={classes.gridRoot}>
                <Grid item xs={12} sm={12} md={6}>
                    <div className={classes.optionDiv}>
                        <h4>Running</h4>

                        <div>
                            <DirectionsRun className={classes.optionIcon} />
                        </div>

                        <p className={classes.smallText}>Record: 17:30</p>
                        <p className={classes.smallText}>Vo2 Max: 66</p>

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

                        <p className={classes.smallText}>Workouts Done: 10</p>
                        <p className={classes.smallText}>Average Duration: 50:00</p>

                        <button className={classes.actionButton} onClick = {() => toggleMode('liveWorkout')}>
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