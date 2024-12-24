import psutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from fpdf import FPDF

# Function to save DataFrame as CSV
def save_as_csv(df, filename="expenses_data.csv"):
    df.to_csv(filename, index=False)
    return filename

# Function to save DataFrame as PDF
def save_as_pdf(df, filename="expenses_data.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for row in df.values:
        pdf.cell(200, 10, txt=str(row), ln=True)
    pdf.output(filename)
    return filename

# Function to dynamically retrieve the Streamlit app URL
def get_streamlit_url():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'streamlit' in proc.info['name']:
            # Check the command line arguments for the port
            for arg in proc.info['cmdline']:
                if '--server.port' in arg:
                    port = arg.split('=')[-1]
                    return f"http://localhost:{port}"
    # Default to 8501 if Streamlit isn't running or port isn't found
    return "http://localhost:8501"

# Function to capture the entire screen as a screenshot
def capture_screenshot(url=None, filename="streamlit_screenshot.png"):
    if url is None:
        url = get_streamlit_url()  # Get dynamic Streamlit URL if not provided
    
    # Set up Selenium to capture the screen
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(180)  # Increased timeout to allow enough time for page load

        # Navigate to the Streamlit app URL
        print(f"Opening URL: {url}")
        driver.get(url)  # Use dynamic URL
        time.sleep(5)  # Allow time for the page to load
        
        # Capture a screenshot
        driver.save_screenshot(filename)
        print(f"Screenshot saved as {filename}")
        
        # Optionally crop or process the image (using Pillow)
        img = Image.open(filename)
        img.save(filename)  # Save the screenshot

    except Exception as e:
        print(f"Error capturing screenshot: {e}")
    finally:
        driver.quit()  # Ensure WebDriver is closed

    return filename


# Example usage
if __name__ == "__main__":
    # Capture screenshot of the Streamlit app
    screenshot_path = capture_screenshot(filename="streamlit_screenshot.png")
    print(f"Screenshot saved at: {screenshot_path}")
