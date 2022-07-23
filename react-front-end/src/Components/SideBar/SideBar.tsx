import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
// import useStyles from './styles';

import {
  AppBar,
  CssBaseline,
  Drawer,
  Hidden,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  Toolbar,
  useTheme,
  Typography, 
  makeStyles
} from '@material-ui/core';

import {
  Dashboard,
  FitnessCenter,
  Event,
  TrackChanges,
  AccountCircle, 
  EmojiFoodBeverageOutlined
} from '@material-ui/icons';

import MenuIcon from '@material-ui/icons/Menu';
import CloseIcon from '@material-ui/icons/Close';
import { Link } from 'react-router-dom';


const paths = [
  {
    'dir': '/dashboard',
    'icon': <Dashboard />,
    'name': 'Dashboard'
  },
  {
    'dir': '/workouts',
    'icon': <FitnessCenter />,
    'name': 'Workouts'
  },
  {
    'dir': '/nutrition',
    'icon': <EmojiFoodBeverageOutlined />,
    'name': 'Nutrition'
  },
  {
    'dir': '/targets',
    'icon': <TrackChanges />,
    'name': 'Targets'
  },
  {
    'dir': '/user-profile',
    'icon': <AccountCircle />,
    'name': 'Profile'
  }
];


const useStyles = makeStyles(theme => ({
  drawer: {
      [theme.breakpoints.up('sm')]: {
          width: 80,
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
      width: 80,
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
}));



function SideBar() {
  const classes = useStyles();
  const theme = useTheme();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  function handleDrawerToggle() {
    setMobileOpen(!mobileOpen)
  }


  const drawer = (
    <div>
      <List>
        {paths.map((path) => (
          <ListItem button key={path.dir}>
            <ListItemIcon>
              <Link to={path.dir} className={classNames(classes.iconLink, window.location.pathname == path.dir && classes.selectedIcon)}>
                {path.icon}
              </Link>
            </ListItemIcon>
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <>
      <AppBar position="fixed" className={classes.appBar}>
        <CssBaseline />

        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="Open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            className={classes.menuButton}
          >
            <MenuIcon />
          </IconButton>

          <Typography variant="h6" noWrap style={{ color: '#022669' }}>
            {paths.filter((element) => element.dir === window.location.pathname)[0].name}
          </Typography>
        </Toolbar>
      </AppBar>

      <nav className={classes.drawer}>
        <Hidden smUp implementation="css">
          <Drawer
            variant="temporary"
            anchor={theme.direction === 'rtl' ? 'right' : 'left'}
            open={mobileOpen}
            onClose={handleDrawerToggle}
            classes={{
              paper: classes.drawerPaper,
            }}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
          >
            <IconButton onClick={handleDrawerToggle} className={classes.closeMenuButton}>
              <CloseIcon />
            </IconButton>
            {drawer}
          </Drawer>
        </Hidden>
        <Hidden xsDown implementation="css">
          <Drawer
            className={classes.drawer}
            variant="permanent"
            classes={{
              paper: classes.drawerPaper,
            }}
          >
            <div className={classes.toolbar} />
            {drawer}
          </Drawer>
        </Hidden>
      </nav>
    </>
  );
}

SideBar.propTypes = {
  container: PropTypes.object,
};

export default SideBar;