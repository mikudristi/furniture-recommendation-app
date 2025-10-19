# Furniture Recommendation AI App

A full-stack web application with AI-powered furniture recommendations, computer vision, and generative AI descriptions.

## Features
- 🤖 ML-based product recommendations
- 🖼️ Computer Vision feature extraction
- 🎨 Generative AI product descriptions
- 📊 Analytics dashboard
- 💬 Conversational recommendation interface

## Tech Stack
- **Backend:** FastAPI, Python, scikit-learn
- **Frontend:** React, Axios
- **AI/ML:** TF-IDF, Cosine Similarity, ResNet, GPT-2
- **Database:** Vector embeddings

## Setup
1. Backend: `cd backend && uvicorn main:app --reload`
2. Frontend: `cd frontend && npm start`

## API Endpoints
- `POST /recommend` - Get product recommendations
- `GET /analytics` - Get dataset analytics
- `GET /products` - Get all products
