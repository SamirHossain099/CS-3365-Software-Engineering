import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./signup.css";

function SignUpIn() {
    const [isSignIn, setIsSignIn] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleToggle = () => {
        setIsSignIn(!isSignIn);
        setError('');
    }

    const handleSubmit = async(e) => {
        e.preventDefault();
        setError('');

        const email = e.target.email.value;
        const password = e.target.password.value;
        const name = isSignIn ? null : e.target.name.value;
        const address = isSignIn ? null : e.target.address.value;
        const phone = isSignIn ? null : e.target.phone.value;

        try {
            const endpoint = isSignIn ? '/users/login/' : '/users/register/';
            const body = isSignIn 
                ? { email, password }
                : { 
                    name,
                    email,
                    password,
                    address,
                    phone: phone
                  };
            
            console.log('Sending request to:', endpoint, 'with body:', body);

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error');
            }

            const data = await response.json();
            localStorage.setItem('user', JSON.stringify(data.user));
            navigate("/home");
        } catch (error) {
            console.error("Error:", error);
            setError(error.message || "An error occurred while connecting to the server");
        }
    }

    return (
        <div>
            <h1>Welcome to Movie Booking System!</h1>
            <h2>{isSignIn ? "Sign In" : "Sign Up"}</h2>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div>
                    {!isSignIn && (
                        <>
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
                    
                    <label htmlFor="email">Email</label>
                    <input type="email" id="email" name="email" required />
                    
                    <label htmlFor="password">Password</label>
                    <input type="password" id="password" name="password" required />
                </div>
                <button type="submit">{isSignIn ? "Sign In" : "Sign Up"}</button>
            </form>
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