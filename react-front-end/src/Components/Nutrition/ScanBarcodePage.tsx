import { useState } from 'react';

import useStyles from './styles';
import { menuProps } from './Nutrition';
import BarcodeScannerComponent from 'react-qr-barcode-scanner';
import RequestHandler from '../RequestHandler/RequestHandler';
import { alertType, CustomAlert, defaultAlertState } from '../CustomAlert/CustomAlert';

import {
    Button, Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Slide,
} from '@material-ui/core';
import { TransitionProps } from '@material-ui/core/transitions';

import { Chart as ChartJS, registerables } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import BackButton from '../BackButton/BackButton';
ChartJS.register(...registerables);


interface dialogType {
    isShow: boolean,
    name: string,
    carbohydrates: { value: number, unit: string },
    protein: { value: number, unit: string },
    fat: { value: number, unit: string },
    calories: { value: number, unit: string },
    servingSize: { value: number, unit: string }, 
    servingNumber: number
};


const defaultDialogState: dialogType = {
    isShow: false,
    name: '',
    carbohydrates: { value: 0, unit: 'g' },
    protein: { value: 0, unit: 'g' },
    fat: { value: 0, unit: 'g' },
    calories: { value: 0, unit: 'g' },
    servingSize: { value: 100, unit: 'g' }, 
    servingNumber: 1
};


function ScanBarcode({ toggleMode }: menuProps) {
    const classes = useStyles();
    const [dialogState, setDialogState] = useState<dialogType>(defaultDialogState);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);

    const closeDialog = () => setDialogState({ ...dialogState, isShow: false });


    function addFoodItem(){
        RequestHandler.POST(
            'food', 
            {
                username: window.localStorage.getItem('username'), 
                token: window.localStorage.getItem('sessionToken'), 
                foodName: dialogState.name, 
                carboHydrates: dialogState.carbohydrates.value * dialogState.servingNumber, 
                protein: dialogState.protein.value * dialogState.servingNumber, 
                fat: dialogState.fat.value * dialogState.servingNumber, 
                calories: dialogState.calories.value * dialogState.servingNumber
            }

        ).then((response) => {
            closeDialog();

            if (response.success){
                setAlertState({isShow: true, isSuccess: true, message: 'Added food item successfully'});
                setTimeout(() => setAlertState({...alertState, isShow: false}), 1500);
            }else{
                setAlertState({isShow: true, isSuccess: false, message: response.message});
                setTimeout(() => setAlertState({...alertState, isShow: false}), 1500);
            }

            setDialogState(defaultDialogState);
        })

    }


    function getBarcodeData(barcode: string) {
        RequestHandler.GET(
            'food-data',
            {
                username: window.localStorage.getItem('username'),
                token: window.localStorage.getItem('sessionToken'),
                queryType: 'barcode',
                barcode: barcode
            }
        ).then((response) => {
            if (response.success) {
                const data = response.data;
                const foodName = data.foodName;
                const servingSize = data.servingSize;
                const nutrients = data.nutrients;

                setDialogState({
                    isShow: true,
                    name: foodName,
                    protein: nutrients.proteins,
                    carbohydrates: nutrients.carbohydrates,
                    fat: nutrients.fat,
                    calories: nutrients.calories,
                    servingSize: servingSize, 
                    servingNumber: 1
                });

            } else {
                setAlertState({isShow: true, isSuccess: false, message: response.message});
                setTimeout(() => setAlertState({...alertState, isShow: false}), 2000);
            }
        })
    }


    return (
        <div className={classes.content}>
            <BackButton callBack={() => toggleMode('menu')} />
            <CustomAlert alertState = {alertState} />

            <h3 className='text-center'>Scan Barcode</h3>

            <Dialog
                open={dialogState.isShow}
                keepMounted
                onClose={closeDialog}
            >
                <DialogTitle>
                    {dialogState.name}
                </DialogTitle>

                <DialogContent>
                    <DialogContentText>
                        Nutritional values per {dialogState.servingSize.value}{dialogState.servingSize.unit}
                    </DialogContentText>

                    <Pie data={{
                        labels: [
                            `Carbohydrates ${dialogState.carbohydrates.unit}`,
                            `Protein ${dialogState.protein.unit}`,
                            `Fat ${dialogState.fat.unit}`
                        ],
                        datasets: [{
                            label: 'Nutrients',
                            data: [dialogState.carbohydrates.value, dialogState.protein.value, dialogState.fat.value],
                            backgroundColor: [
                                'rgb(59, 208, 235)',
                                'rgb(13, 18, 110)',
                                'rgb(85, 11, 110)'
                            ],
                            hoverOffset: 4
                        }]
                    }} />

                    <div className = 'mt-3 text-center'>
                        <p style = {{display: 'inline-block'}}>Serving Number:</p>
                        <input type = 'number'
                               value = {dialogState.servingNumber}
                               className = 'ml-3' 
                               style = {{display: 'inline-block', width: '3vw'}}
                               onChange = {(e) => setDialogState({...dialogState, servingNumber: e.target.value as unknown as number})}>
                        </input> 
                    </div>

                </DialogContent>

                <DialogActions>
                    <Button onClick = {addFoodItem}>Add</Button>
                </DialogActions>
            </Dialog>


            <div className='text-center'>
                <BarcodeScannerComponent
                    width={500}
                    height={500}
                    onUpdate={(err, result) => {
                        if (result) {
                            getBarcodeData(result.getText());
                        }
                    }}
                />
            </div>
        </div>
    );
}

export default ScanBarcode;