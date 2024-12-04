import React from "react";
import { HashRouter as Router,Routes, Route } from "react-router-dom";
import SignUpIn from "./components/signup/signup";
import Home from "./components/home/home";
import ProfilePage from "./components/profile/profilepage";
import Movie from "./components/booking/movie";
import Checkout from "./components/checkout/checkout";

function AppRouter() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<SignUpIn />} />
                <Route path="/home" element={<Home />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/movie/:movieId" element={<Movie />} />
                <Route path="/checkout" element={<Checkout />} />
            </Routes>
        </Router>
    )
}

export default AppRouter;
