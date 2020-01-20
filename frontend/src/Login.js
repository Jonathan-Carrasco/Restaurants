import React, { Component } from "react";
import * as d3 from 'd3';
import axios from "axios";
import { Redirect } from 'react-router';

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {value: '', user: [], redirect: false, username: ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value})
    this.props.onUsernameChange(event.target.value)
    console.log(this.state.value)
  }

  handleSubmit(event) {
    event.preventDefault();
    this.props.onUsernameChange(this.state.value);
    this.setState({redirect: true})
  }

    render() {
      if (this.state.redirect) {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        axios.defaults.xsrfCookieName = "csrftoken";
        axios.get('/api/users/?username='+this.state.value)
             .then(res => {;
               if (res.data === undefined || !res.data.length) {
                 axios.post('/api/users/',{'username': this.state.value, 'timestamp': 0});
                 console.log("array was undefined or length was longer than 0");
                 console.log(res.data);
               }
             })
             .catch(err => console.log(err));

        return <Redirect to='/map' />
    }
        return (
        <form className={'form-inline'} onSubmit={this.handleSubmit}>
          <input className={'form-control input-sm chat-input'} type="text" placeholder="Username" name="username" value={this.state.value} onChange={this.handleChange}></input>
          <button type="submit" className="btn btn-primary btn-md">Login <i className="fa fa-sign-in"></i></button>
        </form>
      )

    }
}

export default Login
