// Importing the various functions from react libraries alongside CSS styling.
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./signup.css";

// Function that creates the SignUp/SignIn page.
function SignUpIn() {
    const [isSignIn, setIsSignIn] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Add useEffect to check existing session on component mount
    useEffect(() => {
        // Clear any existing session when the component mounts
        localStorage.removeItem('user');
        console.log('Cleared existing user session');
    }, []);

    // Function that handles the switch between Sign-In and Sign-Up
    const handleToggle = () => {
        setIsSignIn(!isSignIn);
        setError('');
    }

    // Function that handles the submission method to the backend. Using POST method.
    const handleSubmit = async(e) => {
        e.preventDefault();
        setError('');

        const email = e.target.email.value.trim().toLowerCase();
        const password = e.target.password.value;
        const name = isSignIn ? null : e.target.name.value;
        const address = isSignIn ? null : e.target.address.value;
        const phone = isSignIn ? null : e.target.phone.value;

        try {
            const baseUrl = 'http://localhost:8000';
            const endpoint = isSignIn ? `${baseUrl}/users/login/` : `${baseUrl}/users/register/`;
            
            const body = isSignIn 
                ? { email, password }
                : { name, email, password, address, phone };
            
            console.log('Attempting', isSignIn ? 'login' : 'registration', 'for:', { email });

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(body)
            });

            const data = await response.json();
            console.log('Server response:', data);

            if (!response.ok) {
                throw new Error(data.error || 'Server error');
            }

            // For registration success, attempt immediate login
            if (!isSignIn && data.success) {
                console.log('Registration successful, attempting login...');
                const loginResponse = await fetch(`${baseUrl}/users/login/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify({ email, password })
                });

                const loginData = await loginResponse.json();
                console.log('Login response:', loginData);

                if (!loginResponse.ok) {
                    throw new Error(loginData.error || 'Failed to login after registration');
                }

                if (!loginData.user) {
                    throw new Error('No user data received from login');
                }

                localStorage.setItem('user', JSON.stringify(loginData.user));
            } else if (isSignIn) {
                // Handle direct login
                if (!data.user) {
                    throw new Error('No user data received from login');
                }
                localStorage.setItem('user', JSON.stringify(data.user));
            }

            console.log('Successfully stored user data');
            navigate("/home");
        } catch (error) {
            console.error("Error during authentication:", error);
            setError(error.message);
            localStorage.removeItem('user');
        }
    }

    // This is the HTML elements/info for the Sign-In : Sign-Up page.
    return (
        <div>
            {/* h1 and h2 are headers for the page. (headers like we use in word.) */}
            <h1>Welcome to Movie Booking System!</h1>
            <h2>{isSignIn ? "Sign In" : "Sign Up"}</h2>
            {error && <p className="error-message">{error}</p>}
            {/* Using the form HTML element for sending a group of info. */}
            <form onSubmit={handleSubmit}> {/* Calling the handleSubmit function for when we submit the form. */}
                <div>
                    {!isSignIn && (
                        <>
                            {/* Creating the label and input for the user to enter in their data */}
                            <label htmlFor="name">Name</label>
                            <input type="text" id="name" name="name" required />
                            
                            <label htmlFor="address">Address</label>
                            <input type="text" id="address" name="address" required />
                            
                            <label htmlFor="phone">Phone (10 digits)</label>
                            <input 
                                type="tel" 
                                id="phone" 
                                name="phone" 
                                pattern="[0-9]{10}" 
                                required 
                            />
                        </>
                    )}
                    
                    {/* Creating the rest of the label and inputs for user to enter info. */}
                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" name="email" required />
                    
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" required />
                </div>
                {/* Button that handles the submission of the form. */}
                <button type="submit">{isSignIn ? "Sign In" : "Sign Up"}</button>
            </form>
            {/* Creating section that toggles between Sign-Up and Sign-In for users. */}
            <p>
                {isSignIn ? "Not registered?" : "Already have an account?"}
                <button onClick={handleToggle}>
                    {isSignIn ? "Create an account" : "Sign in"}
                </button>
            </p>
        </div>
    )
}

export default SignUpIn;