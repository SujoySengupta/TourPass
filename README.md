# TourPass - Museum Ticketing System

TourPass is a modern web application that simplifies museum ticket booking and management. It provides an intuitive interface for users to discover museums, purchase tickets, and manage their visits.

## Features

- **User Authentication**
  - Secure login and registration
  - Profile management with customizable avatars
  - Social media integration

- **Museum Discovery**
  - Browse museums with detailed information
  - Search and filter capabilities
  - Interactive maps for museum locations
  - Real-time availability checking

- **Ticket Management**
  - Easy booking process
  - Digital ticket generation
  - QR code support for entry
  - Booking history and upcoming visits

- **User Dashboard**
  - Personal visit statistics
  - Favorite museums
  - Booking management
  - Profile customization

## Technology Stack

- **Backend**
  - Django
  - PostgreSQL
  - Redis (for caching)

- **Frontend**
  - HTML5/CSS3
  - JavaScript
  - Bootstrap 5

- **Authentication**
  - Django Authentication System
  - OAuth2 for social login

## Installation

1. Clone the repository:
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://localhost:8000`
2. Create an account or log in
3. Browse available museums and book tickets
4. Manage your bookings through the dashboard

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Project Link: [https://github.com/yourusername/TourPass](https://github.com/yourusername/TourPass)

## Acknowledgments

- Museum partners
- Open-source community
- All contributors