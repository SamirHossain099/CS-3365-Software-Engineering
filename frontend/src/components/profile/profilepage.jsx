import React, { useState, useEffect } from 'react';
import './profilepage.css';

function ProfilePage() {
    const [userDetails, setUserDetails] = useState({
        name: '',
        email: '',
        password: '',
        address: '',
        phone_number: ''
    });
    const [isEditing, setIsEditing] = useState(false);
    const [editedDetails, setEditedDetails] = useState({});

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userSession = JSON.parse(localStorage.getItem('user'));
                
                if (!userSession || !userSession.id) {
                    console.error('No user session found');
                    return;
                }

                const response = await fetch(`/users/users/${userSession.id}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                });

                if (response.ok) {
                    const userData = await response.json();
                    setUserDetails(userData);
                    setEditedDetails(userData);
                } else {
                    const errorText = await response.text();
                    console.error('Failed to fetch user data:', errorText);
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
            }
        };

        fetchUserData();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEditedDetails(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/users/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    user_id: userDetails.user_id,
                    name: editedDetails.name,
                    email: editedDetails.email,
                    address: editedDetails.address,
                    phone: editedDetails.phone_number
                })
            });

            if (response.ok) {
                const result = await response.json();
                if (result.success) {
                    setUserDetails(editedDetails);
                    setIsEditing(false);
                } else {
                    alert(result.error || 'Failed to update profile');
                }
            } else {
                const errorText = await response.text();
                console.error('Server response:', errorText);
                alert('Failed to update profile');
            }
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile');
        }
    };

    return (
        <div className="profile-container">
            <h1>Profile Page</h1>
            <div className="profile-details">
                {!isEditing ? (
                    // View Mode
                    <>
                        <div className="profile-item">
                            <label>Name:</label>
                            <span>{userDetails.name}</span>
                        </div>
                        <div className="profile-item">
                            <label>Email:</label>
                            <span>{userDetails.email}</span>
                        </div>
                        <div className="profile-item">
                            <label>Address:</label>
                            <span>{userDetails.address}</span>
                        </div>
                        <div className="profile-item">
                            <label>Phone Number:</label>
                            <span>{userDetails.phone_number}</span>
                        </div>
                        <button onClick={() => setIsEditing(true)}>Edit Profile</button>
                    </>
                ) : (
                    // Edit Mode
                    <form onSubmit={handleSubmit}>
                        <div className="profile-item">
                            <label>Name:</label>
                            <input
                                type="text"
                                name="name"
                                value={editedDetails.name}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="profile-item">
                            <label>Email:</label>
                            <input
                                type="email"
                                name="email"
                                value={editedDetails.email}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="profile-item">
                            <label>Address:</label>
                            <input
                                type="text"
                                name="address"
                                value={editedDetails.address}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="profile-item">
                            <label>Phone Number:</label>
                            <input
                                type="tel"
                                name="phone_number"
                                value={editedDetails.phone_number}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="button-group">
                            <button type="submit">Save Changes</button>
                            <button type="button" onClick={() => {
                                setIsEditing(false);
                                setEditedDetails(userDetails);
                            }}>Cancel</button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
}

export default ProfilePage;
