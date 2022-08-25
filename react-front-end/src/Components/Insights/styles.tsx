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
        overflowX: 'hidden'
    },
}));