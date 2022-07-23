import {
    Grid
} from '@material-ui/core';

import {
    DirectionsRun,
    FitnessCenter
} from '@material-ui/icons';

import useStyles from './styles';
import { menuProps } from './Workouts';


function WorkoutMenu({ toggleMode }: menuProps) {
    const classes = useStyles();

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