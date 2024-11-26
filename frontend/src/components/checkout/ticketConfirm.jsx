import PropTypes from 'prop-types';
import React, { useEffect } from 'react';

function TicketConfirmation({ ticketData, onClose }) {
    useEffect(() => {
        const userSession = JSON.parse(localStorage.getItem('user'));
        const userId = userSession?.id;
        
        if (!userId) {
            console.error('No user ID found in session');
            return;
        }

        const existingTickets = JSON.parse(localStorage.getItem(`tickets_${userId}`)) || [];
        
        // Check if ticket already exists
        const ticketExists = existingTickets.some(ticket => ticket.ticketId === ticketData.ticketId);
        
        if (!ticketExists) {
            const updatedTickets = [...existingTickets, ticketData];
            localStorage.setItem(`tickets_${userId}`, JSON.stringify(updatedTickets));
        }
    }, [ticketData]);

    return (
        <>
            <div className="ticket-overlay" onClick={onClose}></div>
            <div className="ticket-dialog">
                <h2>Ticket Confirmation</h2>
                <div className="ticket-details">
                    <p>Ticket ID: {ticketData.ticketId}</p>
                    <p>Movie: {ticketData.movieTitle}</p>
                    <p>Date: {new Date(ticketData.showDate).toLocaleDateString()}</p>
                    <p>Time: {ticketData.showTime}</p>
                    <p>Theater: {ticketData.theaterLocation}</p>
                    <p>Tickets: {ticketData.ticketCount}</p>
                    <p>Total Paid: ${ticketData.totalPrice.toFixed(2)}</p>
                </div>
                <button onClick={onClose}>Close</button>
            </div>
        </>
    );
}

TicketConfirmation.propTypes = {
    ticketData: PropTypes.shape({
        ticketId: PropTypes.string.isRequired,
        movieTitle: PropTypes.string.isRequired,
        showDate: PropTypes.string.isRequired,
        showTime: PropTypes.string.isRequired,
        theaterLocation: PropTypes.string.isRequired,
        ticketCount: PropTypes.number.isRequired,
        totalPrice: PropTypes.number.isRequired
    }).isRequired,
    onClose: PropTypes.func.isRequired
};

export default TicketConfirmation;
