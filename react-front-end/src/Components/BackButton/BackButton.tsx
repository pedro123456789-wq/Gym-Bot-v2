import { Button } from "@material-ui/core";
import {
    ArrowBackIos
} from '@material-ui/icons';
import useStyles from './styles';

interface backButtonProps{
    callBack: () => any

}
function BackButton({callBack}: backButtonProps) {
    const classes = useStyles();

    return (
        <div className = {classes.buttonContainer}>
            <Button
                variant = 'contained'
                className = {classes.button}
                onClick={() => callBack()}
            >
                <ArrowBackIos />
            </Button>
        </div>
    );
}

export default BackButton;