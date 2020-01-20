import React, { Component, } from 'react';
import { Redirect } from 'react-router';
import {Route, NavLink, HashRouter} from "react-router-dom";
import {Navbar, Nav, Container, Row, Col, Form, Button, Input} from "react-bootstrap";

import Home from "./Home";
import MapView from "./MapView";
import MLGraphs from "./MLGraphs";
import Login from "./Login"
import './App.css';
import axios from "axios";

class App extends Component {

  constructor(props) {
      super(props);
      this.handleLogin = this.handleLogin.bind(this);
      this.handleLogout = this.handleLogout.bind(this);
      this.state = {
        restaurant_list: [], /* all restaurants */
        click_list: [],      /* all restaurants the user has clicked */
        username: '',        /* the username passed down to child components */
        value: '',           /* text in the login textbox */
        isLoggedIn: false    /* whether the user has logged in */
      };
  }

  componentDidMount() {
    this.refreshList();
  }

  /* Query restaurants whenever the App component mounts. */
  refreshList = () => {
    axios
      .get("/api/restaurants")
      .then(res => this.setState({ restaurant_list: res.data }))
      .catch(err => console.log(err));
  };

  /* Updates text on the login textbox.  */
  handleChange = (event) => {
    this.setState({value: event.target.value})
  }

  /*
  On submit, the text displayed on the textbox is saved
  as username; The loggedIn boolean then reflects that the
  user has logged in; and if the user hasn't logged in before,
  'username' is added to our database.
   */
  handleLogin = (event) => {

    /* Prevents page from refreshing. */
    event.preventDefault();
    this.setState({username: this.state.value})
    this.setState({isLoggedIn: !this.state.isLoggedIn})

    /* Make an api request after half a second to ensure
       that username is properly saved to state.      */
    setTimeout(() => {

      /* Certificates needed to make a post. */
      axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
      axios.defaults.xsrfCookieName = "csrftoken";

      /* If no user 'username' is found, create a new data
         entry with username 'username' and timestamp 0. */
      axios.get('/api/users/?username='+this.state.usernamw)
           .then(res => {;
             if (res.data === undefined || res.data.length === 0) {
               axios.post('/api/users/',{'username': this.state.username, 'timestamp': 0});
             }
           })
           .catch(err => console.log(err)); }, 500);

    /* Have MapView populate the card deck after a 250 ms. */
    setTimeout(() => { this.mapview.componentDidMount(); }, 250);
  }

  /* On submit, the text displayed on the textbox is erased,
     as well as the username. The isLoggedIn boolean now
     reflects that no user is logged in. Lastly, the card
     deck is cleared. */
  handleLogout = (event) => {
    event.preventDefault();
    this.setState({username: ''})
    this.setState({value: ''})
    this.setState({isLoggedIn: !this.state.isLoggedIn})
    document.getElementById('CardBody').innerHTML = "";
  }

  render() {
    const username = this.state.username;
    return (

        <HashRouter>
            <Navbar bg="dark" variant="dark">
                <Navbar.Brand>Toronto Restaurant Map VDA</Navbar.Brand>
                <Nav className="mr-auto">
                  <Nav.Link href="#/">Home</Nav.Link>
                  <Nav.Link href="#map">Map</Nav.Link>
                  <Nav.Link href="#mlgraphs">MLGraphs</Nav.Link>
                </Nav>
                <Nav className={"navbar-right"}>
                {/* If the user is logged in, display the Logout button and the username.
                    Otherwise, display the text box and Login button.                 */}
                {this.state.isLoggedIn ? (
                  <Form className={'form-inline'} onSubmit={this.handleLogout}>
                    <Navbar.Brand>{this.state.username} is logged in </Navbar.Brand>
                    <Navbar.Brand> </Navbar.Brand>
                    <Button type="submit" className="btn btn-primary btn-md">Logout <i className="fa fa-sign-out"></i></Button>
                  </Form>
                ) : (
                  <Form className={'form-inline'} onSubmit={this.handleLogin}>
                    <Form.Control className={'form-control input-sm chat-input'} type="text" placeholder="Username" name="username" value={this.state.value} onChange={this.handleChange}></Form.Control>
                    <Button type="submit" className="btn btn-primary btn-md">Login <i className="fa fa-sign-in"></i></Button>
                  </Form>
                )}
                </Nav>
            </Navbar>

            <div className="content fill">
                <Container className={"fill"} fluid={true}>
                            <Route exact path={"/"} render={() => <Home restaurant_list={this.state.restaurant_list}/>}/>
                            <Route path={"/map"} render={() => <MapView restaurant_list={this.state.restaurant_list} username={username} onRef={ref => (this.mapview = ref)}/>}/>
                            <Route path={"/mlgraphs"} render={() => <MLGraphs username={username}/>}/>
                </Container>
            </div>
        </HashRouter>
    );
  }
}

export default App;
