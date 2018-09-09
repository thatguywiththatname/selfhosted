"""
Safely serve selfhosted-webserver
"""

from main import app

if __name__ == "__main__":
    print(f"{'*'*10} RUNNING IN DEBUG MODE {'*'*10}")
    app.run(debug=True)
