import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import nltk
from collections import Counter

# Load the pre-trained model
model = MobileNetV2(weights='imagenet')

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

def classify_video_content_and_extract_keywords(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / frame_rate
    print(f"Frame Rate: {frame_rate}, Total Frames: {frame_count}, Duration: {duration} seconds")
    
    all_labels = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize frame to match model input size
        img = cv2.resize(frame, (224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict content in the frame
        preds = model.predict(x)
        decoded_preds = decode_predictions(preds, top=3)[0]
        labels = [pred[1] for pred in decoded_preds]
        
        all_labels.extend(labels)

    cap.release()

    # Determine the most common label (video type)
    most_common_label = Counter(all_labels).most_common(1)[0][0]
    print(f"Video Type: {most_common_label}")

    # Keyword extraction using NLTK
    filtered_labels = [label.replace('_', ' ') for label in all_labels]
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in filtered_labels if word not in stop_words]

    # Top keywords
    top_keywords = Counter(keywords).most_common(100)
    print(f"Top Keywords: {[keyword for keyword, _ in top_keywords]}")

# Path to your video file
video_path = r"C:\Users\ags-008\Downloads\cook.mp4"
classify_video_content_and_extract_keywords(video_path)


# import cv2
# import numpy as np
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
# from tensorflow.keras.preprocessing import image
# import nltk
# from collections import Counter
# from pytube import YouTube
# import os

# # Load the pre-trained model
# model = MobileNetV2(weights='imagenet')

# # Download necessary NLTK data
# nltk.download('stopwords')
# nltk.download('punkt')
# from nltk.corpus import stopwords

# def download_youtube_video(url, output_path="video.mp4"):
#     yt = YouTube(url)
#     # Download the highest resolution stream
#     stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
#     stream.download(filename=output_path)
#     print(f"Downloaded video: {output_path}")

# def classify_video_content_and_extract_keywords(video_path):
#     cap = cv2.VideoCapture(video_path)
#     frame_rate = cap.get(cv2.CAP_PROP_FPS)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     duration = frame_count / frame_rate
#     print(f"Frame Rate: {frame_rate}, Total Frames: {frame_count}, Duration: {duration} seconds")
    
#     all_labels = []
    
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
        
#         # Resize frame to match model input size
#         img = cv2.resize(frame, (224, 224))
#         x = image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         x = preprocess_input(x)

#         # Predict content in the frame
#         preds = model.predict(x)
#         decoded_preds = decode_predictions(preds, top=3)[0]
#         labels = [pred[1] for pred in decoded_preds]
        
#         all_labels.extend(labels)

#     cap.release()

#     # Determine the most common label (video type)
#     most_common_label = Counter(all_labels).most_common(1)[0][0]
#     print(f"Video Type: {most_common_label}")

#     # Keyword extraction using NLTK
#     filtered_labels = [label.replace('_', ' ') for label in all_labels]
#     stop_words = set(stopwords.words('english'))
#     keywords = [word for word in filtered_labels if word not in stop_words]

#     # Top keywords
#     top_keywords = Counter(keywords).most_common(5)
#     print(f"Top Keywords: {[keyword for keyword, _ in top_keywords]}")

# # Example usage
# youtube_url = "https://www.youtube.com/shorts/7Lyx-dQhfRQ"  # Replace with your YouTube video URL
# download_path = "downloaded_video.mp4"

# # Download the YouTube video
# download_youtube_video(youtube_url, output_path=download_path)

# # Analyze the downloaded video
# classify_video_content_and_extract_keywords(download_path)

# # Optionally, remove the video file after processing
# os.remove(download_path)
