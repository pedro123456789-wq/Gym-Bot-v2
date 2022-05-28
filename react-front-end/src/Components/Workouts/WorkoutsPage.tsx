import SideBar from "../SideBar/SideBar";
import {
    CssBaseline,
    useTheme,
    Typography,
    Grid,
    LinearProgress
  } from '@material-ui/core';
  
import {
    DirectionsRun, 
    FitnessCenter
} from '@material-ui/icons';

import useStyles from './styles';



function WorkoutsPage() {
    const classes = useStyles();
    const theme = useTheme();

    return (
        <div>
            <SideBar />
            
            <div className = {classes.content}>
                <Grid container spacing = {2} className = {classes.gridRoot}>
                    <Grid item xs = {12} sm = {12} md = {6}>
                        <div className = {classes.optionDiv}>
                            <h4>Running</h4>
                            
                            <div>
                                <DirectionsRun className = {classes.optionIcon}/>
                            </div>

                            <p className = {classes.smallText}>Record: 17:30</p>
                            <p className = {classes.smallText}>Vo2 Max: 66</p>
                            
                            <button className = {classes.actionButton}>
                                Add Run
                            </button>
                        </div>
                    </Grid>

                    <Grid item xs = {12} sm = {12} md = {6}>
                        <div className = {classes.optionDiv}>
                            <h4>Strength training</h4>

                            <div>
                                <FitnessCenter className = {classes.optionIcon} />
                            </div>

                            <p className = {classes.smallText}>Workouts Done: 10</p>
                            <p className = {classes.smallText}>Average Duration: 50:00</p>

                            <button className = {classes.actionButton}>
                                Start  Workout
                            </button>

                            <button className = {classes.actionButton}>
                                Add workout
                            </button>
                        </div>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default WorkoutsPage;