import {makeStyles} from '@material-ui/core';


export default makeStyles(theme => ({
    radio: {
        '&$checked': {
            color: '#022669'
        }
    }, 
    checked: {}, 
    actionButton: {
        background: '#022669', 
        color: 'white', 
        borderRadius: theme.spacing(1), 
        border: 'none'
    }
}))