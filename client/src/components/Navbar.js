import React from 'react';
import { Link } from 'react-router-dom'
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import RaisedButton from 'material-ui/RaisedButton';

export default class Navbar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {open: false};
    };

    handleToggle = () => this.setState({open: !this.state.open});

    handleClose = () => this.setState({open: false});

    render() {
        return (
            <header>
                <RaisedButton
                    label="Menu"
                    onTouchTap={this.handleToggle}
                />
                <Drawer
                    docked={false}
                    width={200}
                    open={this.state.open}
                    onRequestChange={(open) => this.setState({open})}
                >
                    <Link onTouchTap={this.handleClose} to="/">Home</Link>
                    <Link onTouchTap={this.handleClose} to="/about-us">About</Link>
                    <Link onTouchTap={this.handleClose} to="/login">Login</Link>
                    <Link onTouchTap={this.handleClose} to="/register">Register</Link>
                </Drawer>
            </header>
        );
    }
}