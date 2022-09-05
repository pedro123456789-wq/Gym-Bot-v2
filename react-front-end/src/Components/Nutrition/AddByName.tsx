import { Grid } from '@material-ui/core';
import { useState } from 'react';
import { alertType, CustomAlert, defaultAlertState } from '../CustomAlert/CustomAlert';
import { menuProps } from './Nutrition';
import useStyles from './styles';
import {
    SearchOutlined,
    ArrowRightOutlined,
    ArrowLeftOutlined
} from '@material-ui/icons';
import RequestHandler from '../RequestHandler/RequestHandler';
import { FoodInfo, FoodInfoProps } from './FoodInfo';
import LoadingIndicator from '../LoadingIndicator/LoadingIndicator';
import BackButton from '../BackButton/BackButton';


// Fetch all of the food items at once and store them in the local state then display them page by page
// This is done instead of fetching new items when the user goes to a new page, since it reduces loading times. 

interface pageNavigationType {
    totalPages: number,
    currentPage: number
}

const defaultNavigationState = {
    totalPages: 0,
    currentPage: 0
}


function AddByName({ toggleMode }: menuProps) {
    const classes = useStyles();
    const [alertState, setAlertState] = useState<alertType>(defaultAlertState);
    const [searchQuery, setSearchQuery] = useState('');
    const [foodData, setFoodData] = useState<FoodInfoProps[]>([]);
    const [isLoading, setLoading] = useState<boolean>(false);
    const [pageNavigation, setPageNavigation] = useState<pageNavigationType>(defaultNavigationState);

    function getFoods() {
        setLoading(true);

        RequestHandler.GET(
            'food-data',
            {
                username: window.localStorage.getItem('username'),
                token: window.localStorage.getItem('sessionToken'),
                queryType: 'text', 
                searchQuery: searchQuery,
                resultNumber: 30
            }
        ).then((response) => {
            setLoading(false);

            if (response.success) {
                setFoodData(response.results);
                setPageNavigation({ totalPages: response.results.length / 10, currentPage: 0 });
            } else {
                setAlertState({isShow: true, isSuccess: false, message: response.message});
                setTimeout(() => setAlertState({...alertState, isShow: false}), 2000)
            }
        })
    }

    return (
        <div className={classes.content}>
            <BackButton callBack={() => toggleMode('menu')} />
    
            <h3 className='text-center'>
                Food Search
            </h3>

            <div className='mt-3'>
                <CustomAlert alertState={alertState} />
            </div>

            <div className='mt-4'>
                <Grid container justify='center' alignItems='center' direction='column'>
                    <Grid item xs={12} sm={12} md={12}>
                        <input placeholder='Enter Food Name'
                            className={classes.foodQueryInput}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />

                        <button className='ml-3' style={{ background: 'transparent', border: 'none' }} onClick={() => getFoods()}>
                            <SearchOutlined style={{ color: '#06064a' }} />
                        </button>
                    </Grid>

                    {isLoading ?
                        <Grid item xs={12} sm={12} md={12}>
                            <LoadingIndicator />
                        </Grid>
                        : <div className='mt-5'>
                            {
                                foodData.slice((pageNavigation.currentPage * 10), ((pageNavigation.currentPage * 10) + 10)).map((item) => {
                                    return (
                                        <Grid item xs={12} sm={12} md={6}>
                                            <FoodInfo foodName={item.foodName} nutrients={item.nutrients} servingSize={item.servingSize} />
                                        </Grid>
                                    )
                                })
                            }
                        </div>
                    }

                    {foodData.length > 0 &&
                        <Grid item>

                            <button style={{ display: 'inline-block' }}
                                onClick={() => {
                                    setPageNavigation({ ...pageNavigation, currentPage: pageNavigation.currentPage - 1 })
                                }}
                                disabled={pageNavigation.currentPage == 0}>
                                <ArrowLeftOutlined />
                            </button>


                            <h6 style={{ color: 'black', padding: '3vh', display: 'inline-block' }}>{pageNavigation.currentPage + 1} / {pageNavigation.totalPages}</h6>

                            <button style={{ display: 'inline-block' }}
                                    onClick={() => {
                                        setPageNavigation({ ...pageNavigation, currentPage: pageNavigation.currentPage + 1 })
                                    }}
                                    disabled={pageNavigation.currentPage==pageNavigation.totalPages-1}>
                                <ArrowRightOutlined />
                            </button>
                        </Grid>
                    }
                </Grid>
            </div>
        </div>
    );
}

export default AddByName;