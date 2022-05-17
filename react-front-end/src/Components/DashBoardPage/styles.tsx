export const dashboardStyles = {
    root: {
        display: 'flex',
        background: 'black'
    },
    content: {
        flexGrow: 1,
        paddingTop: theme.spacing(10),
        paddingLeft: theme.spacing(2),
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
        margin: theme.spacing(3)
    },
    dataTitle: {
        color: 'white',
        textAlign: 'center',
        marginTop: theme.spacing(1)
    },
    dataIcon: {
        color: 'white',
        fontSize: theme.spacing(5)
    }
}