import {makeStyles} from '@material-ui/core';


export default makeStyles(theme => ({
    root: {
        display: 'flex',
    },
    content: {
        flexGrow: 1,
        marginTop: theme.spacing(15),
        [theme.breakpoints.up('md')]: {
            marginTop: theme.spacing(20)
        },
        background: '#fafafa'
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
    gridRoot: {
        flexGrow: 1,
        overflowX: 'hidden'
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
    }, 
    foodQueryInput: {
        borderRadius: theme.spacing(1),
        border: 'none', 
        width: '30vw', 
        background: '#06064a', 
        color: 'white', 
        textAlign: 'center', 
        height: '4vh'
    }, 
    foodInfoDiv: {
        background: '#06064a', 
        marginTop: '1vh', 
        borderRadius: theme.spacing(1), 
        width: '60vw'
    }, 
    servingInput: {
        textAlign: 'center', 
        background: 'white', 
        color: 'black', 
        borderRadius: '1vh', 
        borderStyle: 'solid', 
        borderColor: 'black'
    }
}))