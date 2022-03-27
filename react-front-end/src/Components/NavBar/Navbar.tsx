import NavbarItem from './NavbarItem';
import logo from '../../Assets/logo.png';
import { Link } from 'react-router-dom';



function Navbar() : JSX.Element {
    return (
        <nav className = 'navbar navbar-expand-lg navbar-dark'>
            <Link className = 'navbar-brand' to = '/'>
                <div className = 'mt-3'>
                    <img src = {logo} width= '50' height = '45' className = 'd-inline-block align-top' alt=''></img>
                </div>
            </Link>
        
            <button className='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarNav' aria-controls='navbarNav' aria-expanded='false' aria-label='Toggle navigation'>
                <span className='navbar-toggler-icon'></span>
            </button>
            
            <div className = 'collapse navbar-collapse' id = 'navbarNav'>
                <ul className =' navbar-nav'>
                    <NavbarItem path = '/' name  = 'Home'/>
                    <NavbarItem path = '/log-in' name = 'Log In' />
                    <NavbarItem path = '/sign-up' name = 'Sign Up' />
                    <NavbarItem path = '/features' name = 'Features' />
                </ul>
            </div>
        </nav>
    );
}

export default Navbar;