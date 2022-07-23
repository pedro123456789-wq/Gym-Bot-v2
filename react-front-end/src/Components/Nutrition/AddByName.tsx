import { Grid } from '@material-ui/core';
import { useState } from 'react';
import { alertType, CustomAlert, defaultAlertState } from '../CustomAlert/CustomAlert';
import { menuProps } from './Nutrition';
import useStyles from './styles';


function AddByName({ toggleMode }: menuProps) {
    const classes = useStyles();
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);

    return (
        <div className={classes.content}>
            <h3 className='text-center'>
                Food Search
            </h3>

            <div className='mt-3'>
                <CustomAlert alertState={alertState} />
            </div>

            <div>
                <Grid container justify='center' alignItems='center' direction='column'>
                    <Grid item>
                        <div style={{ background: 'black', borderRadius: '3vh', width: '30vw', textAlign: 'center'}}>
                            <input placeholder='Enter Food Name' className='text-center'></input>
                        </div>
                    </Grid>

                </Grid>
            </div>


        </div>
    );
}

export default AddByName;