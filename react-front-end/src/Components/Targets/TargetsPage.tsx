import { Grid, TextField } from "@material-ui/core";
import { EditSharp, DoneSharp } from "@material-ui/icons";
import { useEffect, useState } from "react";
import { classicNameResolver } from "typescript";
import { CustomAlert, alertType, defaultAlertState } from "../CustomAlert/CustomAlert";
import { cammelCaseToText } from "../GlobalVariables";
import LoadingIndicator from "../LoadingIndicator/LoadingIndicator";
import RequestHandler from "../RequestHandler/RequestHandler";
import SideBar from "../SideBar/SideBar";
import useStyles from './styles';


interface targets {
    caloriesEatenTarget: number | null,
    caloriesBurnedTarget: number | null,
    distanceRanTarget: number | null,
    minutesTrainedTarget: number | null
}

const defaultValues: targets = {
    caloriesEatenTarget: null,
    caloriesBurnedTarget: null,
    distanceRanTarget: null,
    minutesTrainedTarget: null
}


function TargetsPage() {
    const classes = useStyles();
    const [targetValues, setTargetValues] = useState<targets>(defaultValues);
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [isLoaded, toggleLoad] = useState<boolean>(false);
    const [canEdit, toggleEdit] = useState<boolean>(false);


    function handleInputChange(e: any) {
        console.log(e.target);
        let {name, value} = e.target;

        if (value === 0) {
            value = null;
        }

        setTargetValues({
            ...targetValues,
            [name]: parseInt(value)
        });
    }


    function fetchTargets() {
        RequestHandler.GET('profile', {
            username: window.localStorage.getItem('username'),
            token: window.localStorage.getItem('sessionToken')
        }).then(response => {
            if (response.success) {
                const responseData = response.data;
                setTargetValues({
                    caloriesEatenTarget: parseInt(responseData.caloriesEatenTarget),
                    caloriesBurnedTarget: parseInt(responseData.caloriesBurnedTarget),
                    distanceRanTarget: parseInt(responseData.distanceRanTarget),
                    minutesTrainedTarget: parseInt(responseData.minutesTrainedTarget)
                });
                toggleLoad(true);
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }
        });
    }


    function saveChages() {
        for (const value of Object.values(targetValues)) {
            if (value === null || isNaN(value) || value === undefined) {
                setAlertState({ isShow: true, isSuccess: false, message: 'You entered some invalid values' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);

                return -1;
            }
        }

        RequestHandler.PUT('profile', {
            ...targetValues, 
            username: window.localStorage.getItem('username'), 
            token: window.localStorage.getItem('sessionToken')
        }).then(response => {
            if (response.success) {
                setAlertState({ isShow: true, isSuccess: true, message: 'Changes Saved' });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
                toggleEdit(false);
            } else {
                setAlertState({ isShow: true, isSuccess: false, message: response.message });
                setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);
                setTimeout(() => setAlertState({ ...alertState, isShow: false }), 2000);
            }
        })
    }



    useEffect(fetchTargets, []);

    return (
        <div>
            <SideBar />

            <div className={classes.content}>
                <h3 className='text-center'>
                    Targets
                </h3>
                
                <div className = 'pt-3'>
                    <CustomAlert alertState={alertState} />
                </div>

                <form>
                    <Grid container direction='column' alignItems='center' justify='center' spacing={2} className='mt-5'>
                        {isLoaded ?
                            Object.entries(targetValues).map(([key, value]) => {
                                return (
                                    <Grid item className='mt-2'>
                                        <TextField
                                            id={key}
                                            name={key}
                                            label={cammelCaseToText(key)}
                                            type='number'
                                            value={value}
                                            onChange={handleInputChange}
                                            margin='normal'
                                            disabled={!canEdit}
                                            className={classes.disabledInput}
                                            fullWidth
                                        />
                                    </Grid>
                                )
                            })

                            : <LoadingIndicator />
                        }
                    </Grid>
                </form>

                <Grid container direction='row' alignItems='center' justify='center' spacing={2}>
                    {canEdit ?
                        <Grid item>
                            <button className={classes.actionButton} style={{ color: 'green' }} onClick = {() => saveChages()}>
                                <DoneSharp className={classes.actionIcon} />
                            </button>
                        </Grid>
                        :
                        <Grid item>
                            <button className={classes.actionButton} onClick={() => toggleEdit(!canEdit)}>
                                <EditSharp className={classes.actionIcon} />
                            </button>
                        </Grid>
                    }
                </Grid>

            </div>
        </div>
    );
}

export default TargetsPage;