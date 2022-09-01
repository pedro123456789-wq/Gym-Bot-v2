import { makeStyles } from "@material-ui/core";

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
        overflowX: 'hidden', 
        [theme.breakpoints.up('md')]: {
            marginLeft: theme.spacing(13)
        }
    }, 
    inputStyle: {
        width: '80%', 
        borderRadius: theme.spacing(1),
        borderStyle: 'solid', 
        borderColor: '#06064a', 
        borderWidth: theme.spacing(0.5),
        textAlign: 'center', 
        marginBottom: theme.spacing(1)
    }, 
    actionButton: {
        width: '60%', 
        background: '#06064a', 
        color: 'white', 
        borderRadius: theme.spacing(3), 
        border: 'none', 
        paddingTop: theme.spacing(1), 
        paddingBottom: theme.spacing(1)
    }, 
    reloadButton: {
        width: '5%', 
        color: '#06064a', 
        background: 'transparent',
        border: 'none'
    }
}));