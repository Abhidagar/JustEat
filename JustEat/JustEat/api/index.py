from app import create_app

app = create_app()

# Handler for serverless function
def handler(request):
    return app(request)
