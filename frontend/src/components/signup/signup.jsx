import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./signup.css";

function SignUpIn() {
    const [isSignIn, setIsSignIn] = useState(true);
    const navigate = useNavigate();

    const handleToggle = () => {
        setIsSignIn(!isSignIn);
    }

    const handleSubmit = async(e) => {
        e.preventDefault();
        const email = e.target.email.value;
        const password = e.target.password.value;

        try {
            const endpoint = isSignIn ? '/api/login/' : '/api/register/';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                    username: email.split('@')[0],
                })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('user', JSON.stringify(data.user));
                navigate("/home");
            } else {
                const error = await response.json();
                alert(error.error);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred.");
        }
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