import cv2
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the track image
image = cv2.imread('tracks/track1.png')  # Replace with your track image path

# Step 2: Convert the image to RGB (OpenCV loads images in BGR format by default)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Step 3: Define the color range for the track (assuming the track is black)
# You can adjust this range based on your track's color.
lower_color = np.array([0, 0, 0])  # Black (for the track)
upper_color = np.array([255, 255, 255])  # Slightly lighter black (for track detection)

# Step 4: Threshold the image to get a binary mask (track vs non-track)
mask = cv2.inRange(image_rgb, lower_color, upper_color)

# Step 5: Extract the track areas using the mask
track_area = cv2.bitwise_and(image_rgb, image_rgb)

# Step 6: Display the original and the tracked image
plt.figure(figsize=(10, 5))

# Original Image
plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title('Original Image')
plt.axis('off')

# Extracted Track Image
plt.subplot(1, 2, 2)
plt.imshow(track_area)
plt.title('Extracted Track Area')
plt.axis('off')

plt.show()

# Optionally, you can save the extracted track area to a new image
cv2.imwrite('extracted_track.png', cv2.cvtColor(track_area, cv2.COLOR_RGB2BGR))
