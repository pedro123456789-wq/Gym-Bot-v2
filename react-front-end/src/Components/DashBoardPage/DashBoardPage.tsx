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
import { Radar, Pie } from 'react-chartjs-2';
import RequestHandler from '../RequestHandler/RequestHandler';
import { useEffect, useState } from 'react';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
import Badge from './Badge';
import { useNavigate } from 'react-router-dom';


ChartJS.register(...registerables)




interface nutrients {
  calories: number,
  protein: number,
  fat: number,
  carboHydrates: number
}

const defaultNutrients: nutrients = {
  calories: 0,
  protein: 0,
  fat: 0,
  carboHydrates: 0
}

interface exercises {
  caloriesBurned: number,
  durationSeconds: number,
}

const defaultExerciseData: exercises = {
  caloriesBurned: 0,
  durationSeconds: 0
}

interface run {
  distanceRan: number,
  durationSeconds: number,
  caloriesBurned: number
}

const defaultRunData: run = {
  distanceRan: 0,
  durationSeconds: 0,
  caloriesBurned: 0
}


interface targets {
  caloriesEatenTarget: number,
  caloriesBurnedTarget: number,
  distanceRanTarget: number,
  minutesTrainedTarget: number
}

const defaultTargetData: targets = {
  caloriesEatenTarget: 0,
  caloriesBurnedTarget: 0,
  distanceRanTarget: 0,
  minutesTrainedTarget: 0
}

interface loadingState {
  profile: boolean,
  food: boolean,
  workouts: boolean,
  targets: boolean,
  runs: boolean
}

const defaultLoadingState: loadingState = {
  profile: false,
  food: false,
  workouts: false,
  targets: false,
  runs: false
}

// TODO:
// Change database to allow user to enter distance in metres
// Add loading indicator to prevent incosistencies
// add separate states for workouts and runs to avoid conflicts

function DashBoardPage() {
  const classes = useStyles();
  const theme = useTheme();
  const [nutrientData, setNutrientData] = useState<nutrients>(defaultNutrients);
  const [workoutData, setWorkoutData] = useState<exercises>(defaultExerciseData);
  const [runData, setRunData] = useState<run>(defaultRunData);
  const [targetData, setTargetData] = useState<targets>(defaultTargetData);
  const [loadingStatus, setLoadingState] = useState<loadingState>(defaultLoadingState);
  const navigate = useNavigate();

  function isShowBadge() {
    return ((workoutData.caloriesBurned + runData.caloriesBurned >= targetData.caloriesBurnedTarget)
      && (workoutData.durationSeconds + runData.durationSeconds >= targetData.minutesTrainedTarget * 60)
      && (runData.distanceRan >= targetData.distanceRanTarget)
      && (nutrientData.calories >= targetData.caloriesEatenTarget));
  }


  function fetchData() {
    setLoadingState({ profile: true, food: true, workouts: true, targets: true, runs: true });

    // get username and token from localStorage 
    const username = window.localStorage.getItem('username');
    const token = window.localStorage.getItem('sessionToken');

    // get targets from database 
    RequestHandler.GET('profile', {
      username: username,
      token: token
    }).then(response => {
      setLoadingState({ ...loadingStatus, profile: false });
      if (response.success) {
        const responseData = response.data;
        setTargetData({
          caloriesEatenTarget: parseInt(responseData.caloriesEatenTarget),
          caloriesBurnedTarget: parseInt(responseData.caloriesBurnedTarget),
          distanceRanTarget: parseFloat(responseData.distanceRanTarget),
          minutesTrainedTarget: parseInt(responseData.minutesTrainedTarget)
        });
      } else {
        alert(response.message);
      }
    });


    // get current date and turn it into string 
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0
    var yyyy = today.getFullYear();

    const startDateString = `${dd}/${mm}/${yyyy}`

    // Get food records 
    RequestHandler.GET('food', {
      username: window.localStorage.getItem('username'),
      token: window.localStorage.getItem('sessionToken'),
      startDate: startDateString,
      endDate: '+1'
    }).then(response => {
      setLoadingState({ ...loadingStatus, food: false })

      if (response.success) {
        const data = response.data

        data.forEach((item: nutrients) => {
          setNutrientData({
            calories: nutrientData.calories + item.calories,
            fat: nutrientData.fat + item.fat,
            carboHydrates: nutrientData.carboHydrates + item.carboHydrates,
            protein: nutrientData.protein + item.protein
          });
        });
      } else {
        alert(response.message);
      }
    });

    // get workouts 
    RequestHandler.GET('workouts', {
      username: window.localStorage.getItem('username'),
      token: window.localStorage.getItem('sessionToken'),
      startDate: startDateString,
      endDate: '+1',
      targetWorkouts: 'ALL'
    }).then(response => {
      setLoadingState({ ...loadingStatus, workouts: false })
      if (response.success) {
        const workouts = response.workouts;
        var totalCalories = 0;
        var totalSeconds = 0;

        for (let workout of workouts) {
          totalCalories += parseInt(workout.caloriesBurned)

          const exercises = workout.exercises;
          for (let exercise of exercises) {
            totalSeconds += parseInt(exercise.durationSeconds)
          }
        }

        setWorkoutData({
          ...workoutData,
          caloriesBurned: totalCalories,
          durationSeconds: totalSeconds
        });

      } else {
        alert(response.message);
      }
    })

    // get runs 
    RequestHandler.GET('runs', {
      username: username,
      token: token,
      startDate: startDateString,
      endDate: '+1'
    }).then(response => {
      setLoadingState({ ...loadingStatus, runs: false });
      if (response.success) {
        const runs = response.data.runs;
        let totalDuration = 0;
        let totalCalories = 0;
        let totalDistance = 0;

        runs.forEach((run: any) => {
          totalDuration += parseInt(run.duration);
          totalCalories += parseInt(run.caloriesBurned);
          totalDistance += parseFloat(run.distance);
        });

        setRunData({
          ...runData,
          durationSeconds: runData.durationSeconds + totalDuration, 
          caloriesBurned: runData.caloriesBurned + totalCalories,
          distanceRan: runData.distanceRan + totalDistance
        });

      } else {
        alert(response.message);
      }
    })
  }

  useEffect(fetchData, []);



  return (
    <div className={classes.root}>
      <CssBaseline />
      <SideBar />
      
      <div className={classes.content}>
        <Typography variant='h5' color='textSecondary' style={{ paddingLeft: '2vw' }}>
          Your Day
        </Typography>

        {Object.values(loadingStatus).includes(true) ?
          <div className='text-center'>
            <LoadingIndicator />
          </div>
          :
          <>
            <Grid container spacing={2} className={classes.gridRoot}>
              <Grid item xs={12} sm={6} md={3}>
                <div className={classes.dataGrid}
                  style={{
                    background: (workoutData.caloriesBurned + runData.caloriesBurned) >=
                      targetData.caloriesBurnedTarget ? '#10de4a' : '#022669'
                  }}
                >
                  <h5 className={classes.dataTitle}>Calories Burned</h5>
                  <Whatshot className={classes.dataIcon} style={{ color: 'red' }} />

                  <div>
                    <LinearProgress
                      classes={{ root: classes.progressBarRoot, bar: classes.progressBarTop }}
                      variant="determinate"
                      value={Math.min(((workoutData.caloriesBurned + runData.caloriesBurned) / targetData.caloriesBurnedTarget) * 100, 100)} />
                  </div>

                  <p className={classes.progressLabel}>{workoutData.caloriesBurned + runData.caloriesBurned} / {targetData.caloriesBurnedTarget}</p>
                </div>
              </Grid>


              <Grid item xs={12} sm={6} md={3}>
                <div className={classes.dataGrid}
                  style={{
                    background: workoutData.durationSeconds + runData.durationSeconds >=
                      targetData.minutesTrainedTarget * 60 ? '#10de4a' : '#022669'
                  }}
                >
                  <h5 className={classes.dataTitle}>Minutes Trained</h5>
                  <ShutterSpeed className={classes.dataIcon} style={{ color: 'gray' }} />

                  <div>
                    <LinearProgress
                      classes={{ root: classes.progressBarRoot, bar: classes.progressBarTop }}
                      variant="determinate"
                      value={Math.min(((workoutData.durationSeconds + runData.durationSeconds) / (targetData.minutesTrainedTarget * 60)) * 100, 100)}
                    />
                  </div>

                  <p className={classes.progressLabel}>{Math.floor((workoutData.durationSeconds + runData.durationSeconds) / 60)} / {targetData.minutesTrainedTarget}</p>
                </div>
              </Grid>


              <Grid item xs={12} sm={6} md={3}>
                <div className={classes.dataGrid}
                  style={{
                    background: runData.distanceRan >=
                      targetData.distanceRanTarget ? '#10de4a' : '#022669'
                  }}
                >
                  <h5 className={classes.dataTitle}>Distance Covered (Km)</h5>
                  <DirectionsRun className={classes.dataIcon} style={{ color: '#2abedb' }} />

                  <div>
                    <LinearProgress
                      classes={{ root: classes.progressBarRoot, bar: classes.progressBarTop }}
                      variant="determinate"
                      value={Math.min((runData.distanceRan / targetData.distanceRanTarget) * 100, 100)} />
                  </div>

                  <p className={classes.progressLabel}>{runData.distanceRan} / {targetData.distanceRanTarget}</p>
                </div>
              </Grid>

              <Grid item xs={12} sm={6} md={3}>
                <div className={classes.dataGrid} style={{
                  background: nutrientData.calories >=
                    targetData.caloriesEatenTarget ? '#10de4a' : '#022669'
                }}>
                  <h5 className={classes.dataTitle}>Calories Eaten</h5>
                  <RestaurantMenu className={classes.dataIcon} style={{ color: '#dea410' }} />

                  <div>
                    <LinearProgress
                      classes={{ root: classes.progressBarRoot, bar: classes.progressBarTop }}
                      variant="determinate"
                      value={(Math.min((nutrientData.calories / targetData.caloriesEatenTarget) * 100, 100))} />
                  </div>

                  <p className={classes.progressLabel}>{nutrientData.calories} / {targetData.caloriesEatenTarget}</p>
                </div>
              </Grid>
            </Grid>

            <Grid container spacing={6} className={classes.gridRoot}>
              <Grid item xs={12} sm={12} md={3}>
                {/* nutrient breakdown  */}
                <div>
                  <h5 className='text-center'>Nutrient breakdown</h5>
                  {(nutrientData.carboHydrates > 0 || nutrientData.protein > 0 || nutrientData.fat > 0) ?
                    <Pie data={{
                      labels: [
                        'Carbohydrates (g)',
                        'Protein (g)',
                        'Fat (g)'
                      ],
                      datasets: [{
                        label: 'Nutrients',
                        data: [nutrientData.carboHydrates, nutrientData.protein, nutrientData.fat],
                        backgroundColor: [
                          'rgb(59, 208, 235)',
                          'rgb(13, 18, 110)',
                          'rgb(85, 11, 110)'
                        ],
                        hoverOffset: 4
                      }]
                    }} />
                    : 
                    <div className='text-center mt-4'>
                      <p style={{ fontFamily: 'Verdana' }}>You have not eaten anything today</p>

                      <button className={classes.actionButton} onClick={() => navigate('/nutrition')}>
                        Add food
                      </button>
                    </div>
                  }
                </div>
              </Grid>

              {/* calories burned breakdown */}
              <Grid item xs={12} sm={12} md={5}>
                {runData.caloriesBurned > 0 || workoutData.caloriesBurned > 0 ?
                  <Radar data={
                    {
                      labels: ['Runs (calories burned)',
                        'Workouts (calories burned)',
                        'Calories Eaten'
                      ],
                      datasets: [{
                        label: 'Caloric breakdown',
                        data: [runData.caloriesBurned, workoutData.caloriesBurned, nutrientData.calories],
                        fill: true,
                        backgroundColor: 'rgba(13, 18, 110, 0.8)'
                      }]
                    }
                  } />
                  :
                  <div className='text-center'>
                    <h5>Caloric breakdown</h5>

                    <p className='mt-4' style={{ fontFamily: 'Verdana' }}>You have not burned any active calories today</p>
                    <button className={classes.actionButton} onClick={() => navigate('/workouts')}>
                      Add workout
                    </button>
                  </div>
                }
              </Grid>

              <Grid item xs={12} sm={12} md={3}>
                <h5 className='text-center'>Training Breakdown</h5>

                {runData.durationSeconds > 0 || workoutData.durationSeconds > 0 ?
                  <Pie data={
                    {
                      labels: [
                        'Running (minutes)',
                        'Workouts (minutes)'
                      ],
                      datasets: [{
                        label: 'Training Breakdown',
                        data: [Math.floor(runData.durationSeconds / 60), Math.floor(workoutData.durationSeconds / 60)],
                        backgroundColor: [
                          'rgb(59, 208, 235)',
                          'rgb(13, 18, 110)',
                        ],
                        hoverOffset: 4
                      }]
                    }
                  } />
                  : 
                  <div className='text-center mt-4'>
                    <p style={{ fontFamily: 'Verdana' }}>You have not trained yet today</p>

                    <button className={classes.actionButton} onClick={() => navigate('/workouts')}>
                      Do Workout
                    </button>
                  </div>}
              </Grid>
            </Grid>

            {isShowBadge() &&
              <Badge />
            }
          </>
        }
      </div>
    </div>
  )
}

export default DashBoardPage;