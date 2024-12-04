# Movie Booking System Project

## Description

This project is a **Movie Booking System (MBS)** developed for a chain of six movie theaters
facing issues with long lines and declining ticket sales. Our solution enables users to conveniently
buy tickets online, with options to print or display them on their personal devices for easy theater access.
Key features include user registration and login, browsing and searching movie catalogs, secure ticket booking,
electronic ticket generation, and user movie reviews.

## Pre - Installation:

Please have [Node.js](https://nodejs.org/en) and [Python](https://python.org/) installed to use the installation process below.

Use Command Prompt on Windows instead of Powershell.

## Installation

1. First create a virtual environment for python libraries.

```
pip install virtualenv
virtualenv myenv
```

2. Activate the virtual environment (NOTE IF VIRTUAL ENVIRONMENT ERRORS OCCUR, you can still run without it. It is just good practice to implement.)

```
myenv\Scripts\activate
```

4. Install the following python libraries from the requirements.txt file.

```
pip install -r requirements.txt
```

5. (OPTIONAL) Install Node.js if not installed on your PC/LAPTOP.
6. Enter the frontend directory and run the following command.

```
cd frontend
```

```
npm install 
```

8. Open up another terminal and enter the backend directory and run the following command to start the backend server.

```
cd backend
```

```
python manage.py migrate
python manage.py runserver
```

9. Enter the frontend directory and run the following command to start the frontend server.

```
npm start
```

10. (OPTIONAL) If you want to login into the admin system, use the following URL and credentials:

```
http://127.0.0.1:8000/admin/

Email: admin@gmail.com
Password: admin
```

## Authors

- [Wesley Spangler](https://github.com/InfiniteWes)
- [Samir Hossain](https://github.com/SamirHossain099)
- [Nicholas Rethans](https://github.com/nrethans)
- Matthew Nunez
- Mateo Blondet
- Rocco Swaney

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
