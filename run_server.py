import uvicorn

def main():
    """Run the FastAPI server."""
    uvicorn.run(
        "api.routes.documents_mock:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload on code changes
    )

if __name__ == "__main__":
    main() 