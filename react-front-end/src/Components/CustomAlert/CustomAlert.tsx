import { Alert } from '@material-ui/lab';
import Snackbar from '@material-ui/core/Snackbar';
import useStyles from './styles';



export interface alertType {
    isShow: boolean,
    isSuccess: boolean,
    message: string
}

export const defaultAlertState: alertType = {
    isShow: false,
    isSuccess: false,
    message: '',
}


type alertProps = {
    alertState: alertType;
}



export function CustomAlert({ alertState }: alertProps) {
    const classes = useStyles();

    return (
        <div>
            {
            alertState.isShow &&
                <div style={{ textAlign: 'left' }}>
                    <Snackbar open={alertState.isShow} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
                        <Alert severity={alertState.isSuccess ? 'success' : 'error'}>
                            {alertState.message}
                        </Alert>
                    </Snackbar>
                </div>

            }
        </div>
    );
}