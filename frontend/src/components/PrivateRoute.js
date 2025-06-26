// PrivateRoute.js
import React from "react";
import { Redirect, Route } from "react-router-dom";

const PrivateRoute = ({ component: Component, ...rest }) => {
  const user = sessionStorage.getItem("user");

  return (
    <Route
      {...rest}
      render={(props) =>
        user ? ( // If user exists in sessionStorage, render the component
          <Component {...props} />
        ) : ( // Otherwise, redirect to the login page
          <Redirect to="/login" />
        )
      }
    />
  );
};

export default PrivateRoute;
