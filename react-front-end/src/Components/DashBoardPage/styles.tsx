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
    dataGrid: {
        background: '#022669',
        zIndex: 1,
        borderRadius: theme.spacing(1),
        margin: theme.spacing(3), 
        textAlign: 'center', 
        padding: theme.spacing(1)
    },
    dataTitle: {
        color: 'white',
        textAlign: 'center',
        marginTop: theme.spacing(1)
    },
    dataIcon: {
        fontSize: theme.spacing(4), 
        textAlign: 'center'
    }, 
    progressBarRoot: {
        marginTop: theme.spacing(3),
        marginBottom: theme.spacing(3),
        height: theme.spacing(1), 
        borderRadius: 5,
        background: 'black'
    }, 
    progressBarTop: {
        borderRadius: 5, 
        background: `linear-gradient(90deg, #702dbd ${100 - 80}%, #e60b29 100%)`
    }, 
    progressLabel: {
        color: 'white', 
        fontSize: theme.spacing(2)
    }, 
    graphDiv: {
        borderWidth: theme.spacing(0.5),
        padding: theme.spacing(1), 
        borderColor: 'gray', 
        borderStyle: 'solid', 
        borderRadius: theme.spacing(0.5), 
        zIndex: 1
    }, 
    actionButton: {
        background: '#022669', 
        color: 'white', 
        borderRadius: '3vh', 
        border: 'none', 
        width: '50%', 
        paddingTop: theme.spacing(0.5), 
        paddingBottom: theme.spacing(0.5)
    }
}));