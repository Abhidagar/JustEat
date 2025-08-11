from app import create_app

app = create_app()

# Vercel needs to import 'app' directly
# Keep the debug run for local development
if __name__ == "__main__":
    app.run(debug=True)
