import React, { Component } from "react";

import axios from "axios";

class Home extends Component {




      renderItems = () => {
        const newItems = this.state.restaurant_list;
        return newItems.map(item => (
          <li key={item.id}
              className="list-group-item d-flex justify-content-between align-items-center">
            <span
            className={`todo-title mr-2`} title={item.name}> {item.mainCategory}
            </span>
          </li>
        ));
      };

    render() {
        return(

            <div>

                <p>There are {this.props.restaurant_list.length} restaurants.</p>

            </div>
        );
    }
}


export default Home;
