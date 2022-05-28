import {makeStyles} from '@material-ui/core';


export default makeStyles(theme => ({
    root: {
        display: 'flex',
    },
    content: {
        flexGrow: 1,
        marginTop: theme.spacing(15),
        [theme.breakpoints.up('md')]: {
            marginTop: theme.spacing(22)
        },
        background: 'white'
    },
    gridRoot: {
        flexGrow: 1,
        overflowX: 'hidden'
    }, 
    optionDiv: {
        background: '#022669',
        borderRadius: theme.spacing(0.5),
        color: 'white', 
        textAlign: 'center',
        padding: theme.spacing(2)
    }, 
    optionIcon: {
        color: 'white', 
        fontSize: theme.spacing(4)
    }, 
    smallText: {
        fontSize: theme.spacing(2), 
        marginTop: theme.spacing(1)
    }, 
    actionButton: {
        background: 'white', 
        color: '#06064a', 
        borderRadius: theme.spacing(0.5),
        border: 'none', 
        fontSize: theme.spacing(2), 
        padding: theme.spacing(1), 
        width: theme.spacing(20),
        margin: theme.spacing(2)
    }

}))