import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import MapView from "./MapView";
const MapApp = () => (
  <DataProvider endpoint="api/restaurants/"
                render={data => <MapView data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<MapApp />, wrapper) : null;
