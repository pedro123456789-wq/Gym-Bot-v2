import SideBar from '../SideBar/SideBar';
import {
  CssBaseline, 
  makeStyles, 
  useTheme,
  Typography, 
  Grid, 
  LinearProgress, 
  OutlinedInput,
  MenuItem, 
  Button, 
  CircularProgress
} from '@material-ui/core';

import {
  Whatshot
} from '@material-ui/icons';

import {Chart as ChartJS, registerables } from 'chart.js';
import {Line} from 'react-chartjs-2';


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




// Chart.register(CategoryScale, Point);

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    background: 'black'
  },
  content: {
    flexGrow: 1,
    paddingTop: theme.spacing(10),
    paddingLeft: theme.spacing(2),
    background: 'white'
  }, 
  gridRoot: {
    flexGrow: 1, 
    overflowX: 'hidden'
  }, 
  dataGrid: {
    background: '#022669', 
    zIndex: 1, 
    borderRadius: theme.spacing(1), 
    margin: theme.spacing(3)
  }, 
  dataTitle: {
    color: 'white', 
    textAlign: 'center',
    marginTop: theme.spacing(1)
  }, 
  dataIcon: {
    color: 'white', 
    fontSize: theme.spacing(5)
  }
}))


function DashBoardPage() {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <div className = {classes.root}>
      <CssBaseline />

      <div>
        <SideBar />
      </div>

      <div className = {classes.content}>
        <Typography variant = 'h5' color = 'textSecondary'>
          Welcome back
        </Typography>

        <Grid container spacing = {2} className = {classes.gridRoot}>
          <Grid item xs = {12} sm = {3}>
            <div className = {classes.dataGrid}>
              <div style = {{display: 'flex', justifyContent: 'space-around'}}>
                <h5 className = {classes.dataTitle}>Calories Burned</h5>
                <Whatshot className = {classes.dataIcon}/>
              </div>

              <p className = 'text-center'>3000 / 4000</p>
            </div>
          </Grid>

          <Grid item xs = {12} sm = {3}>
            <div className = {classes.dataGrid}>
              <div style = {{display: 'flex', justifyContent: 'space-around'}}>
                <h5 className = {classes.dataTitle}>Minutes Trained</h5>
                <Whatshot className = {classes.dataIcon}/>
              </div>
            </div>
          </Grid>

          <Grid item xs = {12} sm = {3}>
            <div className = {classes.dataGrid}>
              <div style = {{display: 'flex', justifyContent: 'space-around'}}>
                <h5 className = {classes.dataTitle}>Distance Covered</h5>
                <Whatshot className = {classes.dataIcon}/>
              </div>
            </div>
          </Grid>

          <Grid item xs = {12} sm = {3}>
            <div className = {classes.dataGrid}>
              <div style = {{display: 'flex', justifyContent: 'space-around'}}>
                  <h5 className = {classes.dataTitle}>Today's Workout</h5>
                  <Whatshot className = {classes.dataIcon}/>
              </div>
            </div>
          </Grid>

          {/* <Grid item xs = {12} sm = {6}>
            <p>
              Time trained
            </p>

            <Line 
              data = {data}
              options = {options}
            />
          </Grid> */}
        </Grid>
      </div>
    </div>
  )
}

export default DashBoardPage;