import { useEffect, useState } from 'react';
import SideBar from "../SideBar/SideBar";
import useStyles from './styles';
import {
    UpdateOutlined
} from '@material-ui/icons';

import { alertType, CustomAlert, defaultAlertState } from '../CustomAlert/CustomAlert';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Line } from 'react-chartjs-2';
import RequestHandler from '../RequestHandler/RequestHandler';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
import { Grid } from '@material-ui/core';
ChartJS.register(...registerables);



const placeholderChartData = {
    labels: [''],
    datasets: [{}]
}


const emptyChart = {
    labels: ['Day1'],
    datasets: [
        {
            label: "Distance Ran (Km)",
            data: [0],
            fill: true,
            groundColor: "rgba(75,192,192,0.2)",
            borderColor: "rgba(75,192,192,1)"
        },
        {
            label: "Time Trained",
            data: [0],
            fill: true,
            groundColor: "rgba(255, 0, 0,1)",
            borderColor: "rgba(255, 0, 0, 1)"
        },
        {
            label: "Calories Eaten",
            data: [0],
            fill: true,
            groundColor: "rgba(0, 255, 0, 1)",
            borderColor: "rgba(0, 255, 0, 1)"
        },
        {
            label: "Calories Burned",
            data: [0],
            fill: true,
            groundColor: "rgba(0, 0, 255, 1)",
            borderColor: "rgba(0, 0, 255, 1)"
        },
    ]
}


const chartOptions = {
    responsive: true,
    scales: {
        x: {
            display: false
        }
    }
}


interface mesurementsType {
    weight: number | null,
    chest: number | null,
    abdomen: number | null,
    hip: number | null
}

const defaultMeasurements: mesurementsType = {
    weight: null,
    chest: null,
    abdomen: null,
    hip: null
}


function InsightsPage() {
    const classes = useStyles();
    const [chartData, setChartData] = useState(placeholderChartData);
    const [startDate, setStartDate] = useState<string>('');
    const [endDate, setEndDate] = useState<string>('');
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [bodyMeasurements, setBodyMeasurements] = useState<mesurementsType>(defaultMeasurements);
    const [bodyFatPrediction, setBodyFatPrediction] = useState<number>(-2);

    function dateToString(date: Date) {
        var dd = String(date.getDate()).padStart(2, '0');
        var mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0
        var yyyy = date.getFullYear();
        return `${dd}/${mm}/${yyyy}`;
    }

    // convert date from server format to html format
    function toHtmlFormat(date: string) {
        let sections = date.split('/');
        return `${sections[2]}-${sections[1]}-${sections[0]}`;
    }

    // convert date from html format to server format
    function toServerFormat(date: string) {
        let sections = date.split('-');
        return `${sections[2].padStart(2, '0')}/${sections[1].padStart(2, '0')}/${sections[0]}`;
    }

    function getData(getDefault: boolean) {
        setChartData(placeholderChartData); //set chart data back to default value to trigger loading indicator

        if (getDefault) {
            // gets called on the first time the data is loaded
            var endDateObj = new Date();
            const interval = (31 * 6);
            var startDateObj = new Date();
            startDateObj.setDate(startDateObj.getDate() - interval);

            var localStartDate = dateToString(startDateObj);
            var localEndDate = dateToString(endDateObj);
        } else {
            // convert data from html to server format to send to server
            var localStartDate = toServerFormat(startDate);
            var localEndDate = toServerFormat(endDate);
        }


        RequestHandler.GET('insights', {
            'username': window.localStorage.getItem('username'),
            'token': window.localStorage.getItem('sessionToken'),
            'startDate': localStartDate,
            'endDate': localEndDate,
        }).then((response) => {
            if (response.success) {
                const data = response.data;
                const distances = data.distance;
                const timeTrained = data.time;
                const caloriesEaten = data.caloriesEaten;
                const caloriesBurned = data.caloriesBurned;

                setStartDate(toHtmlFormat(localStartDate));
                setEndDate(toHtmlFormat(localEndDate));

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
            } else {
                //show default data
                setChartData(emptyChart);
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }, 2000);
            }
        });
    }


    function predictBodyFat() {
        setBodyFatPrediction(-1);  //triggers loading indiciator

        RequestHandler.GET('profile', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken')
        }).then((response) => {
            if (response.success) {
                const weight = response.data.weight;

                RequestHandler.GET('body-fat-prediction',
                    {
                        username: window.localStorage.getItem('username'),
                        token: window.localStorage.getItem('sessionToken'),
                        weight: parseInt(weight),
                        chest: bodyMeasurements.chest,
                        abdomen: bodyMeasurements.abdomen,
                        hip: bodyMeasurements.hip
                    }
                ).then((response) => {
                    if (response.success) {
                        setBodyFatPrediction(response.prediction);
                    } else {
                        setAlertState({ isShow: true, isSuccess: false, message: response.message });
                        setTimeout(() => {
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                            setAlertState({ ...alertState, isShow: false });
                        }, 2000);
                    }
                })
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    setAlertState({ ...alertState, isShow: false });
                }, 2000);
            }
        })
    }


    function getColor(bodyFat: number) {
        if (bodyFat <= 15) {
            return 'green';
        } else if (bodyFat > 15 && bodyFat < 30) {
            return 'yellow';
        } else {
            return 'red';
        }
    }

    useEffect(() => getData(true), [])

    return (
        <div>
            <SideBar />

            <div className={classes.content}>
                <CustomAlert alertState={alertState} />

                <h3 className='text-center pb-4'>
                    Insights
                </h3>

                <Grid container className={classes.gridRoot}>
                    <Grid item xs={12} sm={12} md={7} spacing={3}>
                        {
                            chartData !== placeholderChartData ?
                                <>
                                    <div style={{ display: 'flex', justifyContent: 'center' }}>
                                        <p className='pr-2 mt-3'>From</p>
                                        <input type='date'
                                            value={startDate}
                                            onChange={(e) => setStartDate(e.target.value)}>
                                        </input>

                                        <p className='pl-2 pr-2 mt-3'>to</p>
                                        <input type='date'
                                            value={endDate}
                                            onChange={(e) => setEndDate(e.target.value)}>
                                        </input>

                                        <button onClick={() => getData(false)} className={classes.reloadButton}>
                                            <UpdateOutlined />
                                        </button>
                                    </div>

                                    {/* @ts-ignore */}
                                    <Line data={chartData} options={chartOptions} />
                                </>
                                :
                                <div className='text-center mt-5 pt-5'>
                                    <LoadingIndicator />
                                </div>
                        }
                    </Grid>

                    <Grid xs={12} sm={12} md={4}>
                        <div className='text-center'>
                            <h5>Body Fat Prediction</h5>
                            <input placeholder='Chest circumference (cm)'
                                className={classes.inputStyle}
                                type='number'
                                value={bodyMeasurements.chest || undefined} //required to show placeholder text when no data is entered
                                onChange={(e) => setBodyMeasurements({
                                    ...bodyMeasurements,
                                    chest: e.target.value as unknown as number
                                })}>
                            </input>
                            <input placeholder='Abdomen circumference (cm)'
                                className={classes.inputStyle}
                                type='number'
                                value={bodyMeasurements.abdomen || undefined}
                                onChange={(e) => setBodyMeasurements({
                                    ...bodyMeasurements,
                                    abdomen: e.target.value as unknown as number
                                })}>
                            </input>
                            <input placeholder='Hip circumference (cm)'
                                className={classes.inputStyle}
                                type='number'
                                value={bodyMeasurements.hip || undefined}
                                onChange={(e) => setBodyMeasurements({
                                    ...bodyMeasurements,
                                    hip: e.target.value as unknown as number
                                })}>
                            </input>
                            <button className={classes.actionButton} onClick={predictBodyFat}>Predict Body Fat</button>

                            {
                                bodyFatPrediction > 0 ?
                                    <div style={{
                                        background: getColor(bodyFatPrediction),
                                        borderRadius: '1rem'
                                    }}
                                        className='mt-3 text-center ml-5 mr-5'>
                                        <h5 style={{ color: 'white' }} className = 'pt-2 pb-2'>Body Fat: {bodyFatPrediction}%</h5>
                                    </div>
                                    : bodyFatPrediction == -1 &&
                                    <div>
                                        <LoadingIndicator />
                                    </div>
                            }
                        </div>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default InsightsPage;