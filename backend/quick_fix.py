# quick_fix.py
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("🔧 RUNNING QUICK FIX...")
print("="*50)

# Define the classes first
class QuickRecommender:
    def __init__(self, dataframe):
        self.df = dataframe
        self.vectorizer = TfidfVectorizer(max_features=3000, stop_words='english')
        self.feature_matrix = self.vectorizer.fit_transform(self.df['combined_text'])
        print(f"✅ Model trained! Features: {self.feature_matrix.shape}")
    
    def recommend(self, query, n_recommendations=5):
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.feature_matrix).flatten()
        top_indices = similarities.argsort()[-n_recommendations:][::-1]
        results = self.df.iloc[top_indices].copy()
        results['similarity_score'] = similarities[top_indices]
        return results

class EnhancedFurnitureSystem:
    def __init__(self, recommender):
        self.recommender = recommender
    
    def enhanced_recommend(self, query, n_recommendations=3):
        """
        Get recommendations with AI-generated descriptions
        """
        # Get base recommendations
        recommendations = self.recommender.recommend(query, n_recommendations)
        
        # Add AI-generated descriptions
        enhanced_results = []
        for idx, (_, product) in enumerate(recommendations.iterrows()):
            title = product.get('title', 'Furniture Item')
            category = product.get('categories', 'Furniture').split(',')[0] if pd.notna(product.get('categories')) else 'Furniture'
            
            # Generate creative description
            ai_description = self.generate_product_description(title, category)
            
            enhanced_product = {
                'rank': idx + 1,
                'title': title,
                'original_description': product.get('description', '')[:100] + '...' if pd.notna(product.get('description')) else 'No description',
                'ai_description': ai_description,
                'price': product.get('price', 'N/A'),
                'brand': product.get('brand', 'Unknown'),
                'similarity_score': round(product.get('similarity_score', 0), 3)
            }
            enhanced_results.append(enhanced_product)
        
        return enhanced_results
    
    def generate_product_description(self, product_title, product_category, max_length=100):
        """
        Generate creative product description
        """
        prompts = {
            'Sofa': f"A luxurious {product_title.lower()} that combines modern design with ultimate comfort. Perfect for your living room.",
            'Chair': f"An ergonomic {product_title.lower()} designed for both style and support. Ideal for home or office use.",
            'Table': f"A stunning {product_title.lower()} that brings elegance and functionality to any space. Crafted with care.",
            'Bed': f"A comfortable {product_title.lower()} ensuring restful sleep and modern aesthetics. Your perfect sleep sanctuary.",
            'default': f"A beautifully designed {product_category.lower()} that combines style and functionality. Perfect for modern homes."
        }
        
        category_key = product_category.split(',')[0].strip() if ',' in product_category else product_category
        return prompts.get(category_key, prompts['default'])

# Load your cleaned data
print("📁 Loading cleaned data...")
try:
    df_clean = pd.read_csv('models/cleaned_furniture_data.csv')
    print(f"✅ Data loaded! Shape: {df_clean.shape}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

# Check if combined_text column exists
if 'combined_text' not in df_clean.columns:
    print("🔄 Creating combined_text column...")
    df_clean['combined_text'] = (
        df_clean['title'].fillna('') + ' ' +
        df_clean['description'].fillna('') + ' ' +
        df_clean['categories'].fillna('') + ' ' +
        df_clean['brand'].fillna('') + ' ' +
        df_clean['material'].fillna('') + ' ' +
        df_clean['color'].fillna('')
    )

# Create new model
print("🤖 Creating new recommendation model...")
recommender = QuickRecommender(df_clean)
enhanced_system = EnhancedFurnitureSystem(recommender)

# Save with proper class definitions
print("💾 Saving new model...")
complete_system = {
    'recommender': recommender,
    'enhanced_system': enhanced_system,
    'df_clean': df_clean
}

joblib.dump(complete_system, 'models/complete_furniture_system_fixed.pkl')
print("✅ New model saved as 'models/complete_furniture_system_fixed.pkl'")

# Test it works
print("🧪 Testing new model...")
try:
    results = enhanced_system.enhanced_recommend("office chair", 2)
    print(f"✅ Model test successful! Found {len(results)} recommendations")
    for result in results:
        print(f"   📦 {result['title']} (Score: {result['similarity_score']})")
except Exception as e:
    print(f"❌ Model test failed: {e}")

print("\n🎉 QUICK FIX COMPLETED!")
print("📁 New model file: 'complete_furniture_system_fixed.pkl'")