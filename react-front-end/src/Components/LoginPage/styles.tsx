import {makeStyles} from '@material-ui/core';


export default makeStyles(theme => ({
    actionButton: {
        background: '#06064a', 
        color: 'white', 
        borderRadius: theme.spacing(0.5),
        border: 'none', 
        fontSize: theme.spacing(2), 
        padding: theme.spacing(1), 
        width: theme.spacing(20),
        margin: theme.spacing(2)
    }
}))