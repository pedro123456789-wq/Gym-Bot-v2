import { Grid } from "@material-ui/core";
import Navbar from "../NavBar/Navbar";
import useStyles from './styles';
import {
    WhatshotOutlined,
    FitnessCenterOutlined,
    DirectionsRunOutlined,  
    BlurOnOutlined,   
} from '@material-ui/icons';

function FeaturesPage() {
    const classes = useStyles();

    return (
        <div>
            <Navbar />

            <div>
                <h3 className = 'text-center mt-5'>
                    Features
                </h3>
                
                <div className = 'text-center' style = {{padding: '5vw'}}>
                    <Grid container spacing = {2} alignItems = 'center' justifyContent="center" style={{color: 'white'}}>
                        <Grid item xs = {12} md = {6} sm = {12}>
                            <div className = {classes.featureDiv}>
                                <h5>Calorie Tracking</h5>
                                <p>Track calories eaten and burned</p>
                                <WhatshotOutlined />
                            </div>
                        </Grid>

                        <Grid item xs = {12} md = {6} sm = {12}>
                            <div className = {classes.featureDiv}> 
                                <h5>Gym session tracker</h5>
                                <p>Track gym sessions live or enter your session data</p>
                                <FitnessCenterOutlined />
                            </div>
                        </Grid>

                        <Grid item xs = {12} md = {6} sm = {12}>
                            <div className = {classes.featureDiv}>
                                <h5>Run tracker</h5>
                                <p>Record your runs and track your progress</p>
                                <DirectionsRunOutlined />
                            </div>
                        </Grid>

                        <Grid item xs = {12} md = {6} sm = {12}>
                            <div className = {classes.featureDiv}>
                                <h5>AI Features</h5>
                                <p>HIgh quality, reliable data and smart features to take your fitness to the next level</p>
                                <BlurOnOutlined />
                            </div>
                        </Grid>

                        
                    </Grid>
                </div>
            </div>
        </div>
    );
}

export default FeaturesPage;