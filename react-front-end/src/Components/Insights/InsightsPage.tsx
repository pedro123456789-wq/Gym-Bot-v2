import { useEffect, useState } from 'react';
import SideBar from "../SideBar/SideBar";
import useStyles from './styles';

import { Chart as ChartJS, registerables } from 'chart.js';
import { Line, Radar, Pie } from 'react-chartjs-2';
import RequestHandler from '../RequestHandler/RequestHandler';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
ChartJS.register(...registerables);



const placeholderChartData = {
    labels: [''],
    datasets: [{}]
}


const chartOptions = {
    responsive: true,
    scales: {
        x: {
            display: false
        }
    } 
}


function InsightsPage() {
    const classes = useStyles();
    const [chartData, setChartData] = useState(placeholderChartData);
    const [runDataset, setRunDatset] = useState({});

    function getRunData() {
        RequestHandler.GET('insights', {
            'username': window.localStorage.getItem('username'),
            'token': window.localStorage.getItem('sessionToken'),
            'startDate': '01/02/2022',
            'endDate': '01/08/2022',
        }).then((response) => {
            if (response.success) {
               const data = response.data;
               const distances = data.distance;
               const timeTrained = data.time;
               const caloriesEaten = data.caloriesEaten;
               const caloriesBurned = data.caloriesBurned;

               const chartData = {
                    labels: Object.keys(distances), 
                    datasets: [
                        {
                            label: "Distance Ran (Km)", 
                            data: Object.values(distances), 
                            fill: true, 
                            groundColor: "rgba(75,192,192,0.2)",
                            borderColor: "rgba(75,192,192,1)"
                        }, 
                        {
                            label: "Time Trained", 
                            data: Object.values(timeTrained), 
                            fill: true, 
                            groundColor: "rgba(255, 0, 0,1)",
                            borderColor: "rgba(255, 0, 0, 1)"
                        },
                        {
                            label: "Calories Eaten", 
                            data: Object.values(caloriesEaten), 
                            fill: true, 
                            groundColor: "rgba(0, 255, 0, 1)",
                            borderColor: "rgba(0, 255, 0, 1)"
                        },
                        {
                            label: "Calories Burned", 
                            data: Object.values(caloriesBurned), 
                            fill: true, 
                            groundColor: "rgba(0, 0, 255, 1)",
                            borderColor: "rgba(0, 0, 255, 1)"
                        }, 
                ]
               }

               setChartData(chartData);
            }
        });


        // RequestHandler.GET('')
    }




    useEffect(getRunData, [])


    return (
        <div>
            <SideBar />

            <div className={classes.content}>
                <h3 className='text-center'>
                    Insights
                </h3>

                {/* put inside grid to make chart responsive */}
                <div className = 'ml-5 pl-5' style = {{maxWidth: '70vw'}}>
                    {
                        chartData !== placeholderChartData ?
                            // @ts-ignore
                            <Line data = {chartData} options = {chartOptions}/>
                        : 
                            <div className = 'text-center mt-5 pt-5'>
                                <LoadingIndicator />
                            </div>
                    }
                </div>
            </div>
        </div>
    );
}

export default InsightsPage;