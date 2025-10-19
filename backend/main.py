# main.py - Updated version
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
from typing import List
import uvicorn

# Import from our models module
from models import QuickRecommender, EnhancedFurnitureSystem

print("🚀 Loading ML models...")

try:
    # Load the fixed model
    complete_system = joblib.load('models/complete_furniture_system_fixed.pkl')
    recommender = complete_system['recommender']
    enhanced_system = complete_system['enhanced_system']
    df_clean = complete_system['df_clean']
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    # If loading fails, let's create a simple fallback
    try:
        print("🔄 Trying fallback: creating new model from data...")
        df_clean = pd.read_csv('models/cleaned_furniture_data.csv')
        recommender = QuickRecommender(df_clean)
        enhanced_system = EnhancedFurnitureSystem(recommender)
        print("✅ Fallback model created successfully!")
    except Exception as fallback_error:
        print(f"❌ Fallback also failed: {fallback_error}")
        recommender = None
        enhanced_system = None
        df_clean = None

# Initialize FastAPI app
app = FastAPI(
    title="Furniture Recommendation API", 
    description="AI-powered furniture recommendation system",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class RecommendationRequest(BaseModel):
    query: str
    n_recommendations: int = 5

class ProductResponse(BaseModel):
    rank: int
    title: str
    original_description: str
    ai_description: str
    price: str
    brand: str
    similarity_score: float

class AnalyticsResponse(BaseModel):
    total_products: int
    total_brands: int
    price_stats: dict
    category_distribution: dict

# API Routes
@app.get("/")
async def root():
    return {
        "message": "Furniture Recommendation API is running!",
        "endpoints": {
            "recommendations": "POST /recommend",
            "analytics": "GET /analytics",
            "products": "GET /products"
        }
    }

@app.post("/recommend", response_model=List[ProductResponse])
async def get_recommendations(request: RecommendationRequest):
    """Get product recommendations based on user query"""
    if not enhanced_system:
        raise HTTPException(status_code=500, detail="Recommendation system not loaded")
    
    try:
        print(f"🎯 Getting recommendations for: '{request.query}'")
        results = enhanced_system.enhanced_recommend(
            request.query, 
            request.n_recommendations
        )
        print(f"✅ Found {len(results)} recommendations")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/analytics")
async def get_analytics():
    """Get analytics about the furniture dataset"""
    if df_clean is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")
    
    try:
        # Basic analytics
        total_products = len(df_clean)
        total_brands = df_clean['brand'].nunique() if 'brand' in df_clean.columns else 0
        
        # Price statistics
        price_stats = {}
        if 'price' in df_clean.columns:
            try:
                # Clean price data - handle different price formats
                prices = []
                for price_val in df_clean['price']:
                    if isinstance(price_val, str):
                        # Remove $ and commas, convert to float
                        clean_price = price_val.replace('$', '').replace(',', '').strip()
                        try:
                            prices.append(float(clean_price))
                        except:
                            continue
                    elif isinstance(price_val, (int, float)):
                        prices.append(float(price_val))
                
                if prices:
                    price_stats = {
                        "average_price": round(sum(prices) / len(prices), 2),
                        "min_price": round(min(prices), 2),
                        "max_price": round(max(prices), 2),
                        "median_price": round(sorted(prices)[len(prices)//2], 2)
                    }
            except Exception as price_error:
                price_stats = {"error": f"Price calculation failed: {str(price_error)}"}
        
        # Category distribution (top 10)
        category_dist = {}
        if 'categories' in df_clean.columns:
            try:
                all_categories = df_clean['categories'].fillna('').str.split(',').explode().str.strip()
                top_categories = all_categories.value_counts().head(10).to_dict()
                category_dist = top_categories
            except:
                category_dist = {"error": "Could not process categories"}
        
        return AnalyticsResponse(
            total_products=total_products,
            total_brands=total_brands,
            price_stats=price_stats,
            category_distribution=category_dist
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating analytics: {str(e)}")

@app.get("/products")
async def get_all_products(limit: int = 50, offset: int = 0):
    """Get all products (for analytics page)"""
    if df_clean is None:
        raise HTTPException(status_code=500, detail="Dataset not loaded")
    
    try:
        # Return paginated products with key information
        products = df_clean.iloc[offset:offset + limit].to_dict('records')
        return {
            "products": products,
            "total_products": len(df_clean),
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": enhanced_system is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)