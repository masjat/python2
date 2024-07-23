import streamlit as st
import cv2
import numpy as np

def main():
    st.title("Test Streamlit and OpenCV")
    
    # Create a simple image using NumPy
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    image = cv2.circle(image, (50, 50), 25, (0, 255, 0), -1)  # Draw a green circle
    
    # Convert from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Display image
    st.image(image, caption='Test Image')

if __name__ == "__main__":
    main()
