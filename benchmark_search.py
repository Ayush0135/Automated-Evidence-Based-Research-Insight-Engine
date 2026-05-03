
import time
import http.server
import threading
import os
import sys

# Mock environment variables for search
os.environ["GOOGLE_API_KEY"] = "mock_key"
os.environ["GOOGLE_CSE_ID"] = "mock_cse_id"

import utils.search as search

class MockHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body><h1>Mock Content</h1><p>This is a mock research paper content for benchmarking.</p></body></html>")

    def log_message(self, format, *args):
        return # Silent

def run_server():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MockHandler)
    httpd.serve_forever()

def benchmark():
    # Start local server in a thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1) # Give server time to start

    url = "http://localhost:8000/test"
    iterations = 50

    print(f"Running benchmark with {iterations} iterations...")

    start_time = time.perf_counter()

    for i in range(iterations):
        # Test download_and_parse directly
        search.download_and_parse(url)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Total time for {iterations} downloads: {total_time:.4f}s")
    print(f"Average time per download: {total_time/iterations:.4f}s")

if __name__ == "__main__":
    benchmark()
