import {makeStyles} from '@material-ui/core';


export default makeStyles(theme => ({
    root: {
        display: 'flex',
        background: 'black'
    },
    content: {
        flexGrow: 1,
        paddingTop: theme.spacing(10),
        background: 'white'
    },
    gridRoot: {
        flexGrow: 1,
        overflowX: 'hidden'
    }, 
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