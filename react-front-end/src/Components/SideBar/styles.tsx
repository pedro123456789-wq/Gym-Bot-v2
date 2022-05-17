const drawerWidth = 80;

export const sidebarStyles = {
    drawer: {
        [theme.breakpoints.up('sm')]: {
            width: drawerWidth,
            flexShrink: 0,
        },
    },
    appBar: {
        zIndex: theme.zIndex.drawer + 3,
        background: 'white',
    },
    menuButton: {
        marginRight: theme.spacing(2),
        [theme.breakpoints.up('sm')]: {
            display: 'none',
        },
        color: '#022669'
    },
    toolbar: theme.mixins.toolbar,
    drawerPaper: {
        width: drawerWidth,
        background: '#022669'
    },
    closeMenuButton: {
        marginRight: 'auto',
        marginLeft: '14px',
        color: 'white'
    },
    iconLink: {
        color: 'white',
        paddingLeft: '10px',
        fontSize: '2rem'
    },
    selectedIcon: {
        color: 'purple'
    }
}