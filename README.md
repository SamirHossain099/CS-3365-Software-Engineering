# Movie Booking System Project

## Installation
  1. First create a virtual environment for python libraries.
```
virtualenv myenv
```
  2. Activate the virtual environment
```
myenv\Scripts\activate
```
  4. Install the following python libraries from Django
```
pip install django djangorestframework
```
  5. (OPTIONAL) Install Node.js if not installed on your PC/LAPTOP.
  6. Enter the frontend directory and run the following command.
```
npm install 
```
(This should automatically install the required libraries.)
  8. Enter the backend directory and run the following command to start the backend server.
```
python manage.py migrate
python manage.py runserver
```
  9. Enter the frontend directory and run the following command to start the frontend server.
```
npm run start
```

## Authors
- [Wesley Spangler](https://github.com/InfiniteWes)
- [Samir Hossain](https://github.com/SamirHossain099)
- [Nicholas Rethans](https://github.com/nrethans)
- Matthew Nunez
- Mateo Blondet
- Rocco Swaney

## Description
This project is a **Movie Booking System (MBS)** developed for a chain of six movie theaters
facing issues with long lines and declining ticket sales. Our solution enables users to conveniently
buy tickets online, with options to print or display them on their personal devices for easy theater access.
Key features include user registration and login, browsing and searching movie catalogs, secure ticket booking,
electronic ticket generation, and user movie reviews.
### Key Features
- **User Registration & Login**: Securely register users to manage bookings and personal data.
- **Movie Catalog Browsing & Search**: Display and search for current and upcoming movies with
    details like cast, runtime, and reviews.
- **Ticket Booking**: Users can select showtimes, theater locations, and purchase up to 10 tickets
    per transaction. Accepted payment methods are credit, debit, and PayPal.
- **Electronic Tickets**: Generate a unique barcode or ticket number that users can present at
    the theater for a seamless experience.
- **User Reviews**: Allow users to share feedback on movies and read others' reviews.
- **Admin Functions**: Admins can manage shows, view system status, and ticket sales.

### Technologies
- **Backend**: We use Django for REST API calls, providing a secure and efficient connection
    between the backend and the React frontend.
- **Frontend**: React is used for building an interactive and dynamic user interface with various
    components that enhance the user experience.
- **Data Security**: Django ensures secure handling of data during all transcations and user interactions.
