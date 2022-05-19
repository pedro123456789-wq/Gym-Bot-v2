import SideBar from '../SideBar/SideBar';
import useStyles from './styles';
import {
  CssBaseline,
  useTheme,
  Typography,
  Grid,
  LinearProgress
} from '@material-ui/core';

import {
  Whatshot, 
  ShutterSpeed, 
  DirectionsRun, 
  RestaurantMenu
} from '@material-ui/icons';

import { Chart as ChartJS, registerables } from 'chart.js';
import { Line } from 'react-chartjs-2';


ChartJS.register(...registerables)


const data = {
  labels: ['January', 'February', 'March', 'April', 'May'],
  datasets: [
    {
      label: 'Distance Ran',
      fill: false,
      lineTension: 0.5,
      backgroundColor: 'red',
      borderColor: 'rgba(0,0,0,1)',
      borderWidth: 2,
      data: [65, 59, 80, 81, 56]
    }
  ]
}


const options = {
  responsive: true,
  maintainAspectRatio: true,
  title: {
    display: false,
  },
};



function DashBoardPage() {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <div className={classes.root}>
      <CssBaseline />
      <SideBar />

      <div className={classes.content}>
        <Typography variant='h5' color='textSecondary'>
          Welcome back
        </Typography>

        <Grid container spacing={2} className={classes.gridRoot}>
          <Grid item xs = {12} sm = {6} md = {3}>
            <div className={classes.dataGrid}>
              <h5 className={classes.dataTitle}>Calories Burned</h5>
              <Whatshot className={classes.dataIcon} style = {{color: 'red' }}/>
              
              <div>
                <LinearProgress 
                  classes = {{root: classes.progressBarRoot, bar: classes.progressBarTop}} 
                  variant = "determinate"
                  value = {80}
                />
              </div>

              <p className = {classes.progressLabel}>3000 / 4000</p>
            </div>
          </Grid>


          <Grid item xs = {12} sm = {6} md = {3}>
            <div className={classes.dataGrid}>
              <h5 className={classes.dataTitle}>Minutes Trained</h5>
              <ShutterSpeed className={classes.dataIcon} style = {{color: 'gray'}} />

              <div>
                <LinearProgress 
                  classes = {{root: classes.progressBarRoot, bar: classes.progressBarTop}} 
                  variant = "determinate"
                  value = {60}
                />
              </div>

              <p className = {classes.progressLabel}>3000 / 4000</p>
            </div>
          </Grid>


          <Grid item xs = {12} sm = {6} md = {3}>
            <div className={classes.dataGrid}>
              <h5 className={classes.dataTitle}>Distance Covered</h5>
              <DirectionsRun className={classes.dataIcon} style = {{color: '#2abedb'}}/>
     
              <div>
                <LinearProgress 
                  classes = {{root: classes.progressBarRoot, bar: classes.progressBarTop}} 
                  variant = "determinate"
                  value = {80}
                />
              </div>

              <p className = {classes.progressLabel}>3000 / 4000</p>
            </div>
          </Grid>

          <Grid item xs = {12} sm = {6} md = {3}>
            <div className={classes.dataGrid}>
              <h5 className={classes.dataTitle}>Calories Eaten</h5>
              <RestaurantMenu className={classes.dataIcon} style = {{color: '#1bf207'}}/>

              <div>
                <LinearProgress 
                  classes = {{root: classes.progressBarRoot, bar: classes.progressBarTop}} 
                  variant = "determinate"
                  value = {80}
                />
              </div>

              <p className = {classes.progressLabel}>3000 / 4000</p>
            </div>
          </Grid>

          <Grid item xs = {12} sm = {12} md = {6}>
            <p>
              Time trained
            </p>

            <Line 
              data = {data}
              options = {options}
            />
          </Grid>
        </Grid>
      </div>
    </div>
  )
}

export default DashBoardPage;