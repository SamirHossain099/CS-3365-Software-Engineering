import React, { useEffect, useState } from 'react';
import './profilepage.css';

function ProfilePage() {
    const [userDetails, setUserDetails] = useState({
        name: '',
        email: '',
        password: '',
        address: '',
        phone_number: ''
    });

    useEffect(() => {
        async function fetchUserDetails() {
            const userData = await get_user_details(); // Assume this is a globally available function
            setUserDetails(userData);
        }
        fetchUserDetails();
    }, []);

    return (
        <div className="profile-container">
            <h1>Profile Page</h1>
            <div className="profile-details">
                <div className="profile-item">
                    <label>Name:</label>
                    <span>{userDetails.name}</span>
                </div>
                <div className="profile-item">
                    <label>Email:</label>
                    <span>{userDetails.email}</span>
                </div>
                <div className="profile-item">
                    <label>Password:</label>
                    <span>{userDetails.password}</span>
                </div>
                <div className="profile-item">
                    <label>Address:</label>
                    <span>{userDetails.address}</span>
                </div>
                <div className="profile-item">
                    <label>Phone Number:</label>
                    <span>{userDetails.phone_number}</span>
                </div>
            </div>
        </div>
    );
}

export default ProfilePage;
