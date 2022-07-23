import { Grid } from '@material-ui/core';
import {
    BorderColor,
    CropFree,
    Search
} from '@material-ui/icons';
import useStyles from './styles';
import { menuProps } from './Nutrition';




function NutritionMenu({ toggleMode }: menuProps) {
    const classes = useStyles();

    return (
        <div className={classes.content}>
            <Grid container spacing={2} className={classes.gridRoot}>
                <Grid item xs={12} sm={12} md={6}>
                    <div className={classes.optionDiv}>
                        <h4>
                            Add Manually
                        </h4>

                        <div className={classes.optionIcon}>
                            <BorderColor />
                        </div>

                        <button className={classes.actionButton}
                            onClick={() => toggleMode('manualAdd')}>
                            Add
                        </button>
                    </div>
                </Grid>

                <Grid item xs={12} sm={12} md={6}>
                    <div className={classes.optionDiv}>
                        <h4>
                            Add by name
                        </h4>

                        <div className={classes.optionIcon}>
                            <Search />
                        </div>

                        <button className={classes.actionButton} onClick = {() => toggleMode('nameAdd')}>
                            Add
                        </button>
                    </div>
                </Grid>

                <Grid item xs={12} sm={12} md={12}>
                    <div className={classes.optionDiv}>
                        <h4>
                            Scan Barcode
                        </h4>

                        <div className={classes.optionDiv}>
                            <CropFree />
                        </div>

                        <button className={classes.actionButton}>
                            Add
                        </button>
                    </div>
                </Grid>
            </Grid>
        </div>
    );
}

export default NutritionMenu;