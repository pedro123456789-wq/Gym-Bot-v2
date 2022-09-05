import { Grid, TextField } from '@material-ui/core';
import { useState } from 'react';
import { menuProps } from './Nutrition';

import useStyles from './styles';
import { cammelCaseToText } from '../GlobalVariables';
import RequestHandler from '../RequestHandler/RequestHandler';
import { alertType, defaultAlertState, CustomAlert } from '../CustomAlert/CustomAlert';
import BackButton from '../BackButton/BackButton';


interface foodItem {
    foodName: string | null,
    calories: number | null,
    protein: number | null,
    carboHydrates: number | null,
    fat: number | null
}

const defaultValues: foodItem = {
    foodName: null,
    calories: null,
    protein: null,
    carboHydrates: null,
    fat: null
}


function ManualAddPage({ toggleMode }: menuProps) {
    const classes = useStyles();

    const [foodData, setFoodData] = useState<foodItem>(defaultValues);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);

    function handleInputChange(e: any) {
        let { name, value } = e.target;

        if (value === '') {
            value = null;
        }

        // convert numeric values to numbers
        if (name !== 'foodName') {
            value = parseInt(value);
        }

        setFoodData({
            ...foodData,
            [name]: value,
        });
    }


    function handleSubmit(e: any) {
        e.preventDefault();
        console.log(foodData)

        for (const value of Object.values(foodData)) {
            if (value === null || value === '') {
                setAlertState({ isShow: true, isSuccess: false, message: 'You did not enter some values' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
                return -1;
            }
        }

        RequestHandler.POST('food', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken'),
            foodName: foodData.foodName,
            calories: foodData.calories,
            carboHydrates: foodData.carboHydrates,
            protein: foodData.protein,
            fat: foodData.fat
        }).then((response) => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Added food' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => {
                    setAlertState({ ...alertState, isShow: false });
                    toggleMode('menu');
                }, 1000);
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }
        })
    }


    return (
        <div className={classes.content}>
            <BackButton callBack={() => toggleMode('menu')} />

            <h3 className='text-center'>
                Enter Food Details
            </h3>

            <div className='mt-3'>
                <CustomAlert alertState={alertState} />
            </div>

            <form onSubmit={handleSubmit}>
                <Grid container justify='center' alignItems='center' direction='column'>
                    <Grid item className='mb-2 mt-2'>
                        <TextField
                            id='foodName'
                            name='foodName'
                            label='Food Name'
                            type='text'
                            value={foodData.foodName}
                            onChange={handleInputChange}
                            margin='normal'
                            fullWidth
                        />
                    </Grid>

                    {
                        Object.entries(foodData).slice(1).map(([key, value]) => {
                            return (
                                <Grid item className='mb-2'>
                                    <TextField
                                        id={key}
                                        name={key}
                                        label={cammelCaseToText(key.toLowerCase())}
                                        type='number'
                                        value={value}
                                        onChange={handleInputChange}
                                        margin='normal'
                                        fullWidth
                                    />
                                </Grid>
                            )
                        })
                    }

                    <Grid item className='mt-3'>
                        <input className={classes.actionButton}
                            style={{ 'background': '#022669', 'color': 'white' }}
                            type='submit'
                            value='Add Food'
                        />
                    </Grid>
                </Grid>
            </form>
        </div>
    );
}

export default ManualAddPage;