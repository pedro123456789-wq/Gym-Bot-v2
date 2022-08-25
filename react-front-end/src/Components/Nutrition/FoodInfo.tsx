import { useState } from 'react';
import useStyles from './styles';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import RequestHandler from '../RequestHandler/RequestHandler';
import { alertType, CustomAlert, defaultAlertState } from '../CustomAlert/CustomAlert';

ChartJS.register(...registerables)


export interface FoodInfoProps {
    foodName: string,
    nutrients: {
        protein: { value: number, unit: string },
        carbohydrates: { value: number, unit: string },
        fat: { value: number, unit: string },
        calories: { value: number, unit: string }
    },
    servingSize: { unit: string, value: number },
}


export function FoodInfo({ foodName, nutrients, servingSize }: FoodInfoProps) {
    const classes = useStyles();
    const [showData, setShowData] = useState<boolean>(false);
    const [servingNumber, setServingNumber] = useState<number>(0);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);

    function addFood(foodName: any, nutrients: any, foodItem: any) {
        if (servingNumber === 0) {
            setAlertState({ isShow: true, isSuccess: false, message: 'You must enter the number of servings' });
            setTimeout(() => {
                setAlertState({ ...alertState, isShow: false });
            }, 2000)
        }
        RequestHandler.POST('food', {
            'username': window.localStorage.getItem('username'),
            'token': window.localStorage.getItem('sessionToken'),
            'foodName': foodName,
            'calories': nutrients.calories.value * servingNumber,
            'fat': nutrients.fat.value * servingNumber,
            'carboHydrates': nutrients.carbohydrates.value * servingNumber,
            'protein': nutrients.protein.value * servingNumber
        }).then(response => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Recorded food item' });
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    setShowData(false);
                }, 1000)
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                }, 1000)
            }
        });
    }

    const nutrientBreakdown = {
        labels: [
            'Protein',
            'Carbohydrates',
            'Fat',
        ],
        datasets: [{
            label: '',
            data: [nutrients.protein.value, nutrients.carbohydrates.value, nutrients.fat.value],
            fill: true,
            backgroundColor: ['rgb(255, 99, 132)', 'rgb(239, 242, 56)', 'rgb(18, 12, 36)'],
            borderColor: 'rgb(255, 255, 255)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'
        }],
    };


    return (
        <>
            <CustomAlert alertState={alertState} />

            <div className={classes.foodInfoDiv}>
                <div className='text-center'>
                    <button style={{ border: 'none', background: 'transparent' }} onClick={() => setShowData(!showData)}>
                        <h5 style={{ textAlign: 'center', color: 'white', display: 'inline-block' }}
                            className='pt-3 pb-3'>{foodName}
                        </h5>
                    </button>
                </div>

                {showData &&
                    <div className='text-center'>
                        <div style={{ maxHeight: '10vh' }}>
                            <Pie data={nutrientBreakdown}
                                options={{
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: { legend: { display: false } }
                                }}
                            />
                        </div>

                        <h6 className='mt-3' style={{ color: 'white' }}>Calories: {nutrients.calories.value} {nutrients.calories.unit}</h6>
                        <h6 style={{ color: 'white' }}>Serving size: {servingSize.value} {servingSize.unit}</h6>

                        <input type='number'
                            onChange={(e) => setServingNumber(e.target.value as unknown as number)}
                            placeholder='Number of servings'
                            className={classes.servingInput}>
                        </input>

                        <button className={classes.actionButton} onClick={() => addFood(foodName, nutrients, servingSize)}>
                            Add item
                        </button>
                    </div>
                }
            </div>
        </>
    );
}