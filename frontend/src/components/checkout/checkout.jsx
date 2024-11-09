/**
 * This is the checkout component which will be a dialog box/modal.
 * It will allow us to create a "popup" window for the user to purchase their tickets/seats.
 * The checkout component will have a form for the user to fill out their information.
**/

import "./checkout.css";

function Checkout() {
    const [isPaypal, setIsPaypal] = useState(false);

    return (
        <dialog>
            <h2>Checkout</h2>
            <form>
                {/* Section for the user's information.*/}
                <div>
                    <label htmlFor="Firstname">First Name</label>
                    <input type="text" id="Firstname" name="Firstname" required />
                    <label htmlFor="Lastname">Last Name</label>
                    <input type="text" id="Lastname" name="Lastname" required />
                    <label htmlFor="EmailAddress">Email Address</label>
                    <input type="text" id="EmailAddress" name="EmailAddress" required />
                    <label htmlFor="City">City</label>
                    <input type="text" id="City" name="City" required />
                    <label htmlFor="State">State</label>
                    <input type="text" id="State" name="State" required />
                    <label htmlFor="Zipcode">Zipcode</label>
                    <input type="text" id="Zipcode" name="Zipcode" required />
                </div>
                {/* Section for the user's payment information.*/}
                <div>
                    <label htmlFor="CardNumber">Credit/Debit Card Number</label>
                    <input type="text" id="CardNumber" name="CardNumber" required />
                    <label htmlFor="CardExpiration">Card Expiration</label>
                    <input type="text" id="CardExpiration" name="CardExpiration" required />
                    <label htmlFor="CardSecurityCode">Card Security Code</label>
                    <input type="text" id="CardSecurityCode" name="CardSecurityCode" required />
                </div>
                <button type="submit">Checkout</button>
            </form>
        </dialog>
    )
}

export default Checkout;
