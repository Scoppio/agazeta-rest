import React from 'react';
import { Route } from 'react-router-dom'
import Home from '../home'
import About from '../about'
import Login from '../login'
import Register from '../register'
import Navbar from '../../components/Navbar'

const App = () => (
    <div>
        <Navbar/>
        <main>
            <Route exact path="/" component={Home} />
            <Route exact path="/about-us" component={About} />
            <Route exact path="/login" component={Login} />
            <Route exact path="/register" component={Register} />
        </main>
    </div>
)

export default App