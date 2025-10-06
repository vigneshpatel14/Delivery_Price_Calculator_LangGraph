# 🚚 Delivery Price Calculator API

A FastAPI-based delivery price calculation system with automated email notifications and database persistence. Uses LangGraph for workflow orchestration to calculate delivery costs based on multiple parameters.

## ✨ Features

- **Dynamic Price Calculation**: Calculates delivery prices based on distance, material type, urgency, weight, and location
- **Workflow Orchestration**: Built with LangGraph for clear, maintainable business logic
- **Database Persistence**: SQLite database stores all delivery requests with timestamps
- **Email Notifications**: Automated email confirmations sent to customers
- **RESTful API**: Clean REST endpoints for price calculation and delivery history
- **CORS Enabled**: Ready for frontend integration
- **Interactive Documentation**: Auto-generated Swagger UI at `/docs`

## 🏗️ Architecture

The system uses a graph-based workflow with 8 sequential nodes:

1. **User Input** - Receives and validates delivery request
2. **Distance Calculation** - Calculates base price from distance (₹5/km)
3. **Material Modifier** - Applies material-specific multipliers
4. **Urgency Multiplier** - Applies delivery speed pricing
5. **Weight Surcharge** - Adds charges for heavy items (>5kg)
6. **Location Modifier** - Adjusts for urban/rural delivery
7. **Final Price** - Computes total with all modifiers
8. **Notification** - Sends email confirmation to customer

## 📊 Pricing Logic

### Base Price
- **Distance**: ₹5.00 per kilometer

### Material Type Multipliers
- Standard: 1.0x (no change)
- Fragile: 1.5x
- Perishable: 1.4x
- Heavy: 1.3x

### Urgency Multipliers
- Standard: 1.0x (no change)
- Express: 1.5x
- Same-Day: 2.0x

### Weight Surcharge
- First 5kg: Free
- Additional weight: ₹10 per kg

### Location Modifier
- Urban: 1.0x (no change)
- Rural: 1.2x

### Formula
```
Total Price = ((Base Price × Material × Urgency × Location) + Weight Surcharge)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Gmail account (for email notifications)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/delivery-price-calculator.git
   cd delivery-price-calculator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn fastapi-mail python-dotenv langgraph pydantic
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_app_password
   MAIL_FROM=your_email@gmail.com
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   ```

   **Note**: For Gmail, you need to:
   - Enable 2-Factor Authentication
   - Generate an App Password at https://myaccount.google.com/apppasswords
   - Use the 16-character app password (not your regular password)

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API**
   - API: http://127.0.0.1:8000
   - Interactive Docs: http://127.0.0.1:8000/docs
   - OpenAPI Schema: http://127.0.0.1:8000/openapi.json

## 📡 API Endpoints

### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "API is running!",
  "docs": "/docs"
}
```

### 2. Calculate Delivery Price
```http
POST /calculate-price
```

**Request Body:**
```json
{
  "user_id": "user123",
  "material_type": "fragile",
  "distance": 12.5,
  "urgency": "express",
  "weight": 8.0,
  "location_type": "urban",
  "email": "customer@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "ticket_id": "D-3974",
  "total_price": 123.50,
  "breakdown": {
    "base_price": 62.50,
    "material_modifier": 1.5,
    "urgency_multiplier": 1.5,
    "weight_surcharge": 30.0,
    "location_modifier": 1.0
  },
  "action_log": [
    "Request started: D-3974",
    "Distance: 12.5km -> Base price: $62.50",
    "Material: fragile (x1.5)",
    "Urgency: express (x1.5)",
    "Weight: 8.0kg -> Surcharge: $30.00",
    "Location: urban (x1.0)",
    "TOTAL PRICE: $123.50",
    "Email queued for customer@example.com"
  ],
  "status": "completed"
}
```

### 3. Get Delivery Details
```http
GET /delivery/{ticket_id}
```

**Response:**
```json
{
  "ticket_id": "D-3974",
  "user_id": "user123",
  "material_type": "fragile",
  "distance": 12.5,
  "urgency": "express",
  "weight": 8.0,
  "location_type": "urban",
  "total_price": 123.50,
  "status": "completed",
  "created_at": "2025-10-06T14:30:00.123456"
}
```

### 4. Get All Deliveries
```http
GET /deliveries
```

**Response:**
```json
{
  "total_count": 2,
  "deliveries": [
    {
      "ticket_id": "D-3974",
      "user_id": "user123",
      "material_type": "fragile",
      "distance": 12.5,
      "urgency": "express",
      "weight": 8.0,
      "location_type": "urban",
      "total_price": 123.50,
      "status": "completed",
      "created_at": "2025-10-06T14:30:00.123456"
    }
  ]
}
```

## 🗂️ Project Structure

```
delivery-price-calculator/
│
├── main.py              # FastAPI application and endpoints
├── workflow.py          # LangGraph workflow definition
├── database.py          # SQLite database operations
├── mail_utils.py        # Email notification utilities
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── delivery.db         # SQLite database (auto-created)
```

## 🔧 Configuration

### Material Types
Accepted values: `standard`, `fragile`, `perishable`, `heavy`

### Urgency Levels
Accepted values: `standard`, `express`, `same-day`

### Location Types
Accepted values: `urban`, `rural`

## 📝 Example Usage

### Using cURL
```bash
curl -X POST "http://127.0.0.1:8000/calculate-price" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john_doe",
    "material_type": "fragile",
    "distance": 15.0,
    "urgency": "express",
    "weight": 10.0,
    "location_type": "urban",
    "email": "john@example.com"
  }'
```

### Using Python
```python
import requests

data = {
    "user_id": "john_doe",
    "material_type": "fragile",
    "distance": 15.0,
    "urgency": "express",
    "weight": 10.0,
    "location_type": "urban",
    "email": "john@example.com"
}

response = requests.post("http://127.0.0.1:8000/calculate-price", json=data)
print(response.json())
```

### Using JavaScript (Fetch)
```javascript
const data = {
  user_id: "john_doe",
  material_type: "fragile",
  distance: 15.0,
  urgency: "express",
  weight: 10.0,
  location_type: "urban",
  email: "john@example.com"
};

fetch("http://127.0.0.1:8000/calculate-price", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(data)
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## 🛠️ Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for building APIs
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Workflow orchestration
- **[SQLite](https://www.sqlite.org/)** - Lightweight database
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation
- **[FastAPI Mail](https://sabuhish.github.io/fastapi-mail/)** - Email notifications
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server

## 🐛 Troubleshooting

### Email Not Sending

**Error**: `535, '5.7.8 Username and Password not accepted'`

**Solution**: 
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password at https://myaccount.google.com/apppasswords
3. Use the app password in your `.env` file

### Database Errors

If you see database locked errors, ensure:
- Only one instance of the app is running
- The `delivery.db` file has write permissions

### Port Already in Use

**Error**: `Address already in use`

**Solution**: Change the port:
```bash
uvicorn main:app --reload --port 8001
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- FastAPI documentation and community
- LangGraph for workflow orchestration
- All contributors and users of this project

## 📞 Support

For support, email your.email@example.com or open an issue on GitHub.

---

⭐ If you found this project helpful, please give it a star!
