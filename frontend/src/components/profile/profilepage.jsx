import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './profilepage.css';

function ProfilePage() {
    // Navigation variable
    const navigate = useNavigate();
    const [userDetails, setUserDetails] = useState({
        name: '',
        email: '',
        password: '',
        address: '',
        phone_number: ''
    });
    const [isEditing, setIsEditing] = useState(false);
    const [editedDetails, setEditedDetails] = useState({});
    const [ticketHistory, setTicketHistory] = useState([]);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userSession = JSON.parse(localStorage.getItem('user'));
                
                if (!userSession || !userSession.id) {
                    console.error('No user session found');
                    return;
                }

                console.log('Current user session:', userSession);

                const response = await fetch(`/users/users/${userSession.id}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'include',
                });

                if (response.ok) {
                    const userData = await response.json();
                    console.log('User data:', userData);
                    setUserDetails(userData);
                    setEditedDetails(userData);
                } else {
                    const errorText = await response.text();
                    console.error('Failed to fetch user data:', errorText);
                }

                const [apiTickets, localTickets] = await Promise.all([
                    fetchApiTickets(userSession.id),
                    getLocalStorageTickets(userSession.id)
                ]);

                const combinedTickets = [...apiTickets, ...localTickets].reduce((acc, ticket) => {
                    const id = ticket.booking_id || ticket.ticketId;
                    if (!acc.some(t => (t.booking_id || t.ticketId) === id)) {
                        const normalizedTicket = {
                            booking_id: ticket.booking_id || ticket.ticketId,
                            movie_title: ticket.movie_title || ticket.movieTitle,
                            show_date: ticket.show_date || ticket.showDate,
                            show_time: ticket.show_time || ticket.showTime,
                            theater_location: ticket.theater_location || ticket.theaterLocation,
                            ticket_count: ticket.ticket_count || ticket.ticketCount,
                            total_price: ticket.total_price || ticket.totalPrice
                        };
                        acc.push(normalizedTicket);
                    }
                    return acc;
                }, []);

                setTicketHistory(combinedTickets);
            } catch (error) {
                console.error('Error in fetchUserData:', error);
            }
        };

        fetchUserData();
    }, []);

    const fetchApiTickets = async (userId) => {
        try {
            const ticketsResponse = await fetch(`/booking/user/${userId}/tickets/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'include',
            });

            if (ticketsResponse.ok) {
                const ticketData = await ticketsResponse.json();
                return ticketData.success && ticketData.bookings ? ticketData.bookings : [];
            }
            return [];
        } catch (error) {
            console.error('Error fetching API tickets:', error);
            return [];
        }
    };

    const getLocalStorageTickets = (userId) => {
        try {
            const localTickets = JSON.parse(localStorage.getItem(`tickets_${userId}`)) || [];
            return localTickets;
        } catch (error) {
            console.error('Error getting localStorage tickets:', error);
            return [];
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setEditedDetails(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleLogout = () => {
        localStorage.removeItem('user');
        navigate('/');
    }

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
                        <button onClick={handleLogout}>Logout</button>
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

            <div className="ticket-history">
                <h2>History of Tickets</h2>
                {ticketHistory.length > 0 ? (
                    <div className="tickets-container">
                        {ticketHistory.map((ticket) => (
                            <div key={ticket.booking_id} className="ticket-card">
                                <h3>{ticket.movie_title}</h3>
                                <div className="ticket-info">
                                    <p>Date: {new Date(ticket.show_date).toLocaleDateString()}</p>
                                    <p>Time: {ticket.show_time}</p>
                                    <p>Theater: {ticket.theater_location}</p>
                                    <p>Tickets: {ticket.ticket_count}</p>
                                    <p>Total Paid: ${ticket.total_price}</p>
                                    <p>Booking ID: {ticket.booking_id}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p>No ticket history found.</p>
                )}
            </div>
        </div>
    );
}

export default ProfilePage;
