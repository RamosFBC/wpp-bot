from app import app

# This file is the entry point for the application
# It imports the Flask app from app.py and makes it available for deployment

if __name__ == '__main__':
    # When running directly, start the Flask development server
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
