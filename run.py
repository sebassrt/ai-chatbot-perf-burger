from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Ensure database tables exist when running the app
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting PerfBurger Chatbot...")
    print("📍 Server running at: http://localhost:5000")
    print("💬 Chat endpoint: http://localhost:5000/chat")
    print("🔐 Auth endpoints: http://localhost:5000/users/register, /users/login")
    print("📦 Orders endpoint: http://localhost:5000/orders")
    print("🩺 Health check: http://localhost:5000/health")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
