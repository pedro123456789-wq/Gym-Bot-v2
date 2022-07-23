import { makeStyles } from '@material-ui/core';


export default makeStyles(theme => ({
    content: {
        flexGrow: 1,
        marginTop: theme.spacing(15),
        [theme.breakpoints.up('md')]: {
            marginTop: theme.spacing(15)
        },
        background: '#fafafa'
    },
    gridRoot: {
        flexGrow: 1,
        overflowX: 'hidden'
    },
    disabledInput: {
        "& .MuiInputBase-root.Mui-disabled": {
            color: "black"
        }
    },
    actionButton: {
        background: 'transparent',
        color: '#022669',
        borderRadius: theme.spacing(0.5),
        border: 'none',
        padding: theme.spacing(1),
        width: theme.spacing(20),
        margin: theme.spacing(2), 
    },
    actionIcon: {
        fontSize: '3rem',
        textAlign: 'center'
    }

}));