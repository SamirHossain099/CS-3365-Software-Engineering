/**
 * This is the checkout component which will be a dialog box/modal.
 * It will allow us to create a "popup" window for the user to purchase their tickets/seats.
 * The checkout component will have a form for the user to fill out their information.
**/

import "./checkout.css";
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import TicketConfirmation from './ticketConfirm';

function CheckoutPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const [showTicketDialog, setShowTicketDialog] = useState(false);
    const [ticketData, setTicketData] = useState(null);
    const [paymentMethod, setPaymentMethod] = useState('credit'); // 'credit' or 'paypal'
    const [paymentDetails, setPaymentDetails] = useState({
        cardNumber: '',
        expiryDate: '',
        cvv: '',
        cardholderName: '',
        paypalEmail: ''
    });
    
    // Get checkout data from navigation state
    const {
        showtimeId,
        ticketPrice,
        ticketCount,
        movieTitle,
        showDate,
        showTime,
        theaterLocation
    } = location.state || {};

    // If no data, redirect to home
    if (!showtimeId) {
        navigate('/');
        return null;
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setPaymentDetails(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handlePurchaseComplete = async (e) => {
        e.preventDefault();
        
        // Validate payment details
        if (paymentMethod === 'credit') {
            if (!paymentDetails.cardNumber || !paymentDetails.expiryDate || !paymentDetails.cvv || !paymentDetails.cardholderName) {
                alert('Please fill in all credit card details');
                return;
            }
        } else if (paymentMethod === 'paypal' && !paymentDetails.paypalEmail) {
            alert('Please enter PayPal email');
            return;
        }

        try {
            // Get user data from localStorage
            const userString = localStorage.getItem('user');
            const user = userString ? JSON.parse(userString) : null;
            
            // Check if user exists
            if (!user) {
                alert('Please log in to complete your purchase');
                navigate('/login');
                return;
            }

            const userId = user.id || user.pk;
            const csrfToken = getCookie('csrftoken');

            if (!userId) {
                console.error('User ID not found:', user);
                alert('Authentication error. Please log in again.');
                navigate('/login');
                return;
            }

            // Generate a UUID instead of timestamp
            const ticketId = crypto.randomUUID(); // This generates a proper UUID
            
            console.log('Sending booking request with data:', {
                user_id: userId,
                showtime_id: showtimeId,
                ticket_count: ticketCount,
                total_price: ticketCount * ticketPrice,
                ticket_id: ticketId
            });

            const response = await fetch('http://localhost:8000/booking/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    user_id: userId,
                    showtime_id: showtimeId,
                    ticket_count: ticketCount,
                    total_price: ticketCount * ticketPrice,
                    ticket_id: ticketId,
                    showDate: showDate,
                    showTime: showTime,
                    theaterLocation: theaterLocation,
                    payment_method: paymentMethod,
                    payment_details: paymentMethod === 'credit' ? {
                        card_number: paymentDetails.cardNumber,
                        expiry_date: paymentDetails.expiryDate,
                        cvv: paymentDetails.cvv,
                        cardholder_name: paymentDetails.cardholderName
                    } : {
                        paypal_email: paymentDetails.paypalEmail
                    }
                }),
                credentials: 'include',
            });

            const data = await response.json();
            console.log('Booking response:', data);

            if (!response.ok) {
                throw new Error(data.error || 'Failed to create booking');
            }

            // Set ticket data and show confirmation dialog
            setTicketData({
                ticketId: data.booking.ticket_id,
                movieTitle: data.booking.movie_title,
                showDate: data.booking.show_date,
                showTime: data.booking.show_time,
                theaterLocation: data.booking.theater_location,
                ticketCount: data.booking.ticket_count,
                totalPrice: parseFloat(data.booking.total_price)
            });
            setShowTicketDialog(true);

        } catch (error) {
            console.error('Booking error:', error);
            alert(error.message || 'An error occurred during booking');
        }
    };

    // Helper function to get cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    return (
        <div className="checkout-page">
            <h1>Checkout</h1>
            <div className="checkout-details">
                <h2>Order Summary</h2>
                <p>Movie: {movieTitle}</p>
                <p>Date: {new Date(showDate).toLocaleDateString()}</p>
                <p>Time: {showTime}</p>
                <p>Theater: {theaterLocation}</p>
                <p>Number of Tickets: {ticketCount}</p>
                <p>Price per Ticket: ${ticketPrice}</p>
                <p>Total Price: ${(ticketCount * ticketPrice).toFixed(2)}</p>
                
                <h2>Payment Method</h2>
                <div className="payment-selection">
                    <label>
                        <input
                            type="radio"
                            name="paymentMethod"
                            value="credit"
                            checked={paymentMethod === 'credit'}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                        />
                        Credit Card
                    </label>
                    <label>
                        <input
                            type="radio"
                            name="paymentMethod"
                            value="paypal"
                            checked={paymentMethod === 'paypal'}
                            onChange={(e) => setPaymentMethod(e.target.value)}
                        />
                        PayPal
                    </label>
                </div>

                {paymentMethod === 'credit' ? (
                    <div className="credit-card-form">
                        <input
                            type="text"
                            name="cardholderName"
                            placeholder="Cardholder Name"
                            value={paymentDetails.cardholderName}
                            onChange={handleInputChange}
                        />
                        <input
                            type="text"
                            name="cardNumber"
                            placeholder="Card Number"
                            maxLength="16"
                            value={paymentDetails.cardNumber}
                            onChange={handleInputChange}
                        />
                        <input
                            type="text"
                            name="expiryDate"
                            placeholder="MM/YY"
                            maxLength="5"
                            value={paymentDetails.expiryDate}
                            onChange={handleInputChange}
                        />
                        <input
                            type="text"
                            name="cvv"
                            placeholder="CVV"
                            maxLength="3"
                            value={paymentDetails.cvv}
                            onChange={handleInputChange}
                        />
                    </div>
                ) : (
                    <div className="paypal-form">
                        <input
                            type="email"
                            name="paypalEmail"
                            placeholder="PayPal Email"
                            value={paymentDetails.paypalEmail}
                            onChange={handleInputChange}
                        />
                    </div>
                )}
                
                <button onClick={handlePurchaseComplete}>
                    Complete Purchase
                </button>
            </div>

            {showTicketDialog && ticketData && (
                <TicketConfirmation 
                    ticketData={ticketData}
                    onClose={() => {
                        setShowTicketDialog(false);
                        navigate('/');
                    }}
                />
            )}
        </div>
    );
}

export default CheckoutPage;
