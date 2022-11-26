import {Link} from 'react-router-dom'


type NavBarItemProps = {
    path : string, 
    name : string, 
};



function NavbarItem({path, name} : NavBarItemProps) : JSX.Element {
    return (
        <div>
             <li className = {`nav-item 
                              ${window.location.pathname === path && 'active'}`}>
                <Link className = 'nav-link' to = {path}>
                    {name}
                    {window.location.pathname === path && 
                        <span className='sr-only'>
                            (current)
                        </span>}
                </Link>
            </li>
        </div>  
    );
}

export default NavbarItem;