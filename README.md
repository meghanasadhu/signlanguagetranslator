# Two-Way Indian Sign Language Translator using LSTM and NLP

This repository contains the official implementation of our published research paper:  

> **Two Way Indian Sign Language Translator using LSTM and NLP**  
> Authors: Ch. Rakesh, G. Madhumitha, S. Meghana, T. Sahithi Niharika, M. Rohith, Ajay Ram K.  
> Published in: International Journal for Research in Applied Science & Engineering Technology (IJRASET), Volume 11, Issue V, May 2023.  

📄 Read the full paper here: [IJRASET – Two Way Indian Sign Language Translator using LSTM and NLP](https://www.ijraset.com/best-journal/two-way-indian-sign-language-translator-using-lstm-and-nlp)

---

## 📌 Overview

The project introduces a **bi-directional translator** for Indian Sign Language (ISL), enabling communication between the deaf/mute community and the general public through two modules:

1. **Sign-to-Text**: Detects ISL gestures in real time via webcam/video input, extracts keypoints using **MediaPipe Holistic**, and predicts the corresponding text using an **LSTM-based deep learning model**.  
2. **Text-to-Sign**: Processes user text input, applies **NLP preprocessing** (tokenization, lemmatization), and maps words to pre-recorded ISL sign video clips to generate continuous sign sequences.

---

## ✨ Key Features

- Recognizes **15 ISL phrases/actions** (e.g., *Good Morning, Thank You Very Much, How Are You*).  
- Achieved **~88% accuracy** in real-time sign-to-text translation using an LSTM model.  
- Handles **paragraph-level input** for text-to-sign translation, outputting concatenated sign videos.  
- Uses **MediaPipe + OpenCV** for gesture detection and **MoviePy** for sign video concatenation.  
- Real-time **webcam support** for sign capture and translation.  

---

## 🏗️ System Architecture

### 1. Data Collection & Preprocessing
- Videos recorded via webcam/OpenCV (~50 samples per sign).  
- Each video split into 20 frames.  
- Extracted pose, hand, and face keypoints using **MediaPipe Holistic**.  
- Saved feature arrays for model training.  

### 2. Sign-to-Text Model
- Built with **4 LSTM layers** + **4 Dense layers**.  
- ~732k trainable parameters.  
- Trained on sequential keypoint data for temporal gesture recognition.  

### 3. Text-to-Sign Module
- Tokenizes and lemmatizes input text.  
- Looks up pre-recorded ISL video clips for each token.  
- Concatenates videos into a continuous sign output.  

### 4. Deployment
- **Web UI** for real-time sign detection and text input.  
- Simple interface for end users to translate both ways.

---

## 🚀 Usage

### Installation
```bash
# Clone the repository
git clone https://github.com/meghanasadhu/signlanguagetranslator.git
cd signlanguagetranslator

# Install dependencies
pip install -r requirements.txt

# Training the LSTM Model
python train_sign_to_text.py

# Running the Application
python app.py

