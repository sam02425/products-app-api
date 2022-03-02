import { Fragment } from "react";
import HeaderCartButton from "./HeaderCartButton"; 
import classes from './Header.module.css'
import mealsImage from '../../assets/meals.jpeg'


const Header = props => {
    return(
        <Fragment>
            <header className={classes.header}>
                <h1>Tadka Stand</h1>
                <HeaderCartButton onClick={props.onShowCart}/>
            </header>
            <div className={classes['main-image']}>
                <img src={mealsImage} alt='A tabel full of delicious food!'/>
            </div>
        </Fragment>
    );
};

export default Header;