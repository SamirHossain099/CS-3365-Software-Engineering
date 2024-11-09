import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./signup.css";

function SignUpIn() {
    const [isSignIn, setIsSignIn] = useState(true);
    const navigate = useNavigate();

    const handleToggle = () => {
        setIsSignIn(!isSignIn);
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const email = e.target.email.value;
        const password = e.target.password.value;

        console.log(email, password);
        navigate("/home");
    }

    return (
        <div>
            <h1>Welcome to Movie Booking System!</h1>
            <h2>{isSignIn ? "Sign In" : "Sign Up"}</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="email">Email</label>
                    <input type="text" id="email" name="email" />
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" />
                </div>
                <button type="submit">{isSignIn ? "Sign In" : "Sign Up"}</button>
            </form>
            <p>
                {isSignIn ? "Not registered?" : "Already have an account?"}
                <button onClick={handleToggle}>{isSignIn ? "Create an account" : "Sign in"}</button>
            </p>
        </div>
    )
}

export default SignUpIn;