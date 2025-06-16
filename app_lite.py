import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Smart Agriculture Framework",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #228B22;
        margin-bottom: 1rem;
    }
    .prediction-result {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class SmartAgricultureApp:
    def __init__(self):
        self.rbca_rules = {
            'rice': {'temperature': (20, 27), 'humidity': (80, 85), 'ph': (5.5, 7.0), 'N': (60, 100), 'P': (35, 60), 'K': (35, 45), 'rainfall': (150, 300)},
            'wheat': {'temperature': (12, 25), 'humidity': (50, 70), 'ph': (6.0, 7.5), 'N': (50, 80), 'P': (30, 50), 'K': (30, 50), 'rainfall': (75, 180)},
            'maize': {'temperature': (18, 27), 'humidity': (55, 75), 'ph': (5.5, 7.0), 'N': (60, 100), 'P': (35, 60), 'K': (15, 25), 'rainfall': (60, 110)},
            'cotton': {'temperature': (21, 30), 'humidity': (70, 85), 'ph': (5.8, 8.0), 'N': (100, 150), 'P': (40, 70), 'K': (15, 30), 'rainfall': (50, 100)},
            'banana': {'temperature': (26, 30), 'humidity': (75, 85), 'ph': (6.0, 7.5), 'N': (100, 150), 'P': (75, 100), 'K': (300, 400), 'rainfall': (100, 180)},
            'grapes': {'temperature': (15, 25), 'humidity': (60, 70), 'ph': (6.0, 7.0), 'N': (50, 80), 'P': (30, 50), 'K': (200, 250), 'rainfall': (50, 100)},
            'apple': {'temperature': (15, 25), 'humidity': (50, 60), 'ph': (5.5, 7.0), 'N': (20, 40), 'P': (125, 150), 'K': (200, 250), 'rainfall': (100, 180)},
            'mango': {'temperature': (27, 35), 'humidity': (50, 70), 'ph': (5.5, 7.5), 'N': (10, 40), 'P': (10, 40), 'K': (20, 50), 'rainfall': (50, 100)},
            'orange': {'temperature': (15, 30), 'humidity': (50, 70), 'ph': (6.0, 7.5), 'N': (10, 40), 'P': (10, 40), 'K': (10, 40), 'rainfall': (100, 120)},
            'chickpea': {'temperature': (20, 25), 'humidity': (60, 70), 'ph': (6.0, 7.5), 'N': (40, 60), 'P': (60, 80), 'K': (20, 40), 'rainfall': (60, 90)},
            'kidney_beans': {'temperature': (15, 25), 'humidity': (60, 70), 'ph': (6.0, 7.0), 'N': (20, 40), 'P': (60, 80), 'K': (20, 40), 'rainfall': (60, 90)},
            'coconut': {'temperature': (25, 30), 'humidity': (70, 80), 'ph': (5.5, 7.0), 'N': (70, 100), 'P': (30, 50), 'K': (50, 80), 'rainfall': (100, 200)},
            'papaya': {'temperature': (25, 30), 'humidity': (60, 70), 'ph': (6.0, 7.0), 'N': (50, 80), 'P': (30, 50), 'K': (50, 70), 'rainfall': (100, 150)},
            'jute': {'temperature': (25, 35), 'humidity': (75, 85), 'ph': (6.0, 7.5), 'N': (80, 120), 'P': (40, 60), 'K': (20, 40), 'rainfall': (150, 250)},
            'coffee': {'temperature': (15, 25), 'humidity': (70, 80), 'ph': (6.0, 6.5), 'N': (100, 120), 'P': (20, 40), 'K': (20, 40), 'rainfall': (150, 200)}
        }
    
    def calculate_rbca_score(self, crop, params):
        if crop not in self.rbca_rules:
            return 0.0
        
        rules = self.rbca_rules[crop]
        total_score = 0
        weights = {'temperature': 0.25, 'humidity': 0.20, 'ph': 0.15, 'N': 0.15, 'P': 0.10, 'K': 0.10, 'rainfall': 0.05}
        
        for param, value in params.items():
            if param in rules and param in weights:
                min_val, max_val = rules[param]
                if min_val <= value <= max_val:
                    param_score = 1.0
                else:
                    if value < min_val:
                        param_score = max(0, 1 - (min_val - value) / min_val)
                    else:
                        param_score = max(0, 1 - (value - max_val) / max_val)
                total_score += param_score * weights[param]
        
        return min(1.0, total_score)
    
    def get_crop_recommendations(self, params):
        scores = {}
        for crop in self.rbca_rules:
            scores[crop] = self.calculate_rbca_score(crop, params)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def main():
    app = SmartAgricultureApp()
    
    st.markdown('<h1 class="main-header">🌾 Smart Agriculture Framework</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Advanced AI-Powered Crop Recommendation System</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="warning-box">ℹ️ Running in RBCA-only mode (lightweight version) - Full functionality available - v1.1</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("## 🌱 Farm Parameters")
    st.sidebar.markdown("Enter your farm's environmental and soil conditions:")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        nitrogen = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=80, step=1)
        phosphorus = st.number_input("Phosphorus (P)", min_value=0, max_value=150, value=45, step=1)
        potassium = st.number_input("Potassium (K)", min_value=0, max_value=400, value=35, step=1)
        temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
    
    with col2:
        humidity = st.number_input("Humidity (%)", min_value=0, max_value=100, value=75, step=1)
        ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=150.0, step=1.0)
    
    predict_button = st.sidebar.button("🔮 Get Crop Recommendations", type="primary")
    
    if predict_button:
        input_params = {
            'N': nitrogen, 'P': phosphorus, 'K': potassium,
            'temperature': temperature, 'humidity': humidity,
            'ph': ph, 'rainfall': rainfall
        }
        
        tab1, tab2, tab3 = st.tabs(["🎯 Recommendations", "📊 Analysis", "📈 Visualizations"])
        
        with tab1:
            st.markdown("## Crop Recommendations")
            recommendations = app.get_crop_recommendations(input_params)
            
            col1, col2, col3 = st.columns(3)
            for i, (crop, score) in enumerate(recommendations[:3]):
                with [col1, col2, col3][i]:
                    st.markdown(f"""
                    <div class="prediction-result">
                        <h3>#{i+1} {crop.replace('_', ' ').title()}</h3>
                        <h2 style="color: #2E8B57;">{score:.1%}</h2>
                        <p>Suitability Score</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("### 📋 Detailed Suitability Analysis")
            rec_df = pd.DataFrame(recommendations, columns=['Crop', 'Suitability Score'])
            rec_df['Crop'] = rec_df['Crop'].str.replace('_', ' ').str.title()
            rec_df['Suitability Score'] = rec_df['Suitability Score'].apply(lambda x: f"{x:.1%}")
            rec_df['Rank'] = range(1, len(rec_df) + 1)
            rec_df = rec_df[['Rank', 'Crop', 'Suitability Score']]
            st.dataframe(rec_df, use_container_width=True)
        
        with tab2:
            st.markdown("## Parameter Analysis")
            best_crop = recommendations[0][0]
            optimal_ranges = app.rbca_rules[best_crop]
            
            comparison_data = []
            for param in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
                if param in optimal_ranges:
                    min_val, max_val = optimal_ranges[param]
                    current_val = input_params[param]
                    status = "✅ Optimal" if min_val <= current_val <= max_val else "⚠️ Suboptimal"
                    comparison_data.append({
                        'Parameter': param.title(),
                        'Your Value': current_val,
                        'Optimal Range': f"{min_val} - {max_val}",
                        'Status': status
                    })
            
            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df, use_container_width=True)
            
            conf_fig = go.Figure(data=[
                go.Bar(x=[crop.replace('_', ' ').title() for crop, _ in recommendations[:10]],
                       y=[score for _, score in recommendations[:10]],
                       marker_color=px.colors.sequential.Viridis)
            ])
            conf_fig.update_layout(title="Top 10 Crop Suitability Confidence Scores", xaxis_title="Crops", yaxis_title="Confidence Score", height=400)
            st.plotly_chart(conf_fig, use_container_width=True)
        
        with tab3:
            st.markdown("## Advanced Visualizations")
            
            fig = make_subplots(rows=2, cols=2, subplot_titles=('Soil Nutrients (NPK)', 'Environmental Conditions', 'Soil pH Level', 'Parameter Summary'), specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "indicator"}, {"type": "bar"}]])
            
            fig.add_trace(go.Bar(x=['Nitrogen', 'Phosphorus', 'Potassium'], y=[input_params['N'], input_params['P'], input_params['K']], marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'], name='NPK'), row=1, col=1)
            fig.add_trace(go.Bar(x=['Temperature (°C)', 'Humidity (%)', 'Rainfall (mm)'], y=[input_params['temperature'], input_params['humidity'], input_params['rainfall']], marker_color=['#FFA07A', '#98D8C8', '#87CEEB'], name='Environment'), row=1, col=2)
            fig.add_trace(go.Indicator(mode="gauge+number", value=input_params['ph'], domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Soil pH"}, gauge={'axis': {'range': [None, 14]}, 'bar': {'color': "#2E8B57"}, 'steps': [{'range': [0, 6], 'color': "lightgray"}, {'range': [6, 8], 'color': "lightgreen"}, {'range': [8, 14], 'color': "lightgray"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 7}}), row=2, col=1)
            
            all_params = ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall']
            all_values = [input_params['N'], input_params['P'], input_params['K'], input_params['temperature'], input_params['humidity'], input_params['ph'], input_params['rainfall']]
            fig.add_trace(go.Bar(x=all_params, y=all_values, marker_color=px.colors.qualitative.Set3, name='All Parameters'), row=2, col=2)
            fig.update_layout(height=600, showlegend=False, title_text="Agricultural Parameter Analysis")
            st.plotly_chart(fig, use_container_width=True)
            
            categories = ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall']
            normalized_values = []
            for param in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
                val = input_params[param]
                if param in ['N', 'P', 'K']:
                    normalized_values.append(min(val / 100, 1.0))
                elif param == 'temperature':
                    normalized_values.append(min(val / 40, 1.0))
                elif param == 'humidity':
                    normalized_values.append(val / 100)
                elif param == 'ph':
                    normalized_values.append(val / 14)
                elif param == 'rainfall':
                    normalized_values.append(min(val / 300, 1.0))
            
            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(r=normalized_values, theta=categories, fill='toself', name='Your Farm Parameters', line_color='#2E8B57'))
            radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, title="Farm Parameter Profile", height=500)
            st.plotly_chart(radar_fig, use_container_width=True)
    
    else:
        st.markdown("""
        ## 🚀 Welcome to the Smart Agriculture Framework
        
        This advanced AI-powered system helps farmers make informed decisions about crop selection based on:
        
        ### 🔬 **Advanced Technologies**
        - **RBCA Engine**: Rule-Based Context-Aware recommendations
        - **Comprehensive Database**: 15+ crop types with optimal growing conditions
        - **Real-time Analysis**: Instant suitability scoring
        - **Interactive Visualizations**: Beautiful charts and analysis
        
        ### 📊 **Key Features**
        - Real-time crop suitability analysis
        - Multi-parameter optimization
        - Visual parameter analysis
        - Confidence scoring
        - Optimal range recommendations
        
        ### 🌱 **Supported Crops**
        Rice, Wheat, Maize, Cotton, Banana, Grapes, Apple, Mango, Orange, Chickpea, Kidney Beans, Coconut, Papaya, Jute, Coffee
        
        ### 🌱 **How to Use**
        1. Enter your farm's soil and environmental parameters in the sidebar
        2. Click "Get Crop Recommendations" to analyze your conditions
        3. Explore different tabs for detailed insights and visualizations
        
        ---
        
        **Ready to optimize your farming decisions? Enter your parameters and get started!**
        """)
        
        st.markdown("### 📋 Parameter Guidelines")
        sample_col1, sample_col2 = st.columns(2)
        
        with sample_col1:
            st.markdown("""
            **Soil Nutrients:**
            - Nitrogen (N): 0-200 kg/ha
            - Phosphorus (P): 0-150 kg/ha  
            - Potassium (K): 0-400 kg/ha
            """)
        
        with sample_col2:
            st.markdown("""
            **Environmental Conditions:**
            - Temperature: 0-50°C
            - Humidity: 0-100%
            - pH: 0-14 (6-8 optimal for most crops)
            - Rainfall: 0-500mm
            """)

if __name__ == "__main__":
    main() 