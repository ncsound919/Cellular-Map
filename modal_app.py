import modal

app = modal.App("cellular-map")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("gcc", "g++")
    .pip_install(
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "pydantic==2.6.0",
        "pydantic-settings==2.1.0",
        "biopython==1.83",
        "networkx==3.3",
        "numpy==1.26.3",
        "pandas==2.2.0",
        "scikit-learn==1.4.0",
        "httpx==0.26.0",
        "python-dotenv==1.0.0",
        "aiofiles==23.2.1",
        "python-multipart==0.0.6",
        "requests==2.31.0",
    )
)

@app.function(image=image)
@modal.web_endpoint(method="GET")
def health():
    return {"status": "ok", "service": "cellular-map"}

@app.function(image=image)
@modal.web_endpoint(method="GET")
def info():
    return {"name": "Cellular-Map", "version": "1.0.0", "runtime": "Modal"}
