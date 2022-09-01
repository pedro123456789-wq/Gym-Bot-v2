import {
    CheckCircle,
} from '@material-ui/icons';

function Badge() {
    return (
        <div style={{ background: '#10de4a' }} className='text-center'>
            <h5 className='pt-3' style = {{color: 'white'}}>Great Work!</h5>
            <p style = {{color: 'white'}}>You reached all your targets for today</p>
            <CheckCircle className='mb-3' style = {{color: 'white', fontSize: '2rem'}}/>
        </div>
    );
}

export default Badge;