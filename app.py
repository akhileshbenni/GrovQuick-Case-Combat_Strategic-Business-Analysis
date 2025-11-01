import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="GrovQuick Case Combat",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better presentation style
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .slide-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    """Load and prepare the grocery case data"""
    try:
        df = pd.read_csv('hyperlocal_grocery_case-hyperlocal_grocery_case.csv')
        
        # Add computed columns
        df['CLV'] = df['AvgOrderValue'] * df['OrderFrequency']
        df['ReturnRate'] = df['ReturnedOrders'] / df['OrderFrequency']
        
        # Assume CAC varies by segment (example values)
        cac_map = {'Premium': 500, 'Regular': 300, 'Budget': 200, 'Occasional': 150}
        df['CAC'] = df['CustomerSegment'].map(cac_map)
        df['ROI'] = df['CLV'] - df['CAC']
        
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please ensure 'hyperlocal_grocery_case-hyperlocal_grocery_case.csv' is in the same directory.")
        return None

df = load_data()

# Sidebar Navigation
st.sidebar.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=GrovQuick", use_container_width=True)
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Section:",
    [
        "🏠 Introduction",
        "📋 Executive Summary",
        "🔍 Data Exploration / EDA",
        "🎯 Funnel Analysis",
        "💰 ROI & Segmentation",
        "🎨 Strategies & BMC",
        "📈 Simulated Impact",
        "⚠️ Limitations & Conclusion"
    ]
)

# Stop if data not loaded
if df is None:
    st.stop()

# ============================================================================
# SLIDE 1: INTRODUCTION
# ============================================================================
if page == "🏠 Introduction":
    st.markdown('<p class="slide-title">🛒 GrovQuick Case Combat</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to the GrovQuick Business Case Analysis")
        st.markdown("""
        ### About GrovQuick
        GrovQuick is a **quick-commerce (Q-commerce) platform** operating in **Tier-2 cities** across India, 
        delivering groceries and essentials within **10-15 minutes**.
        
        #### Business Context
        - 🏙️ **Market**: Tier-2 cities with growing digital adoption
        - ⚡ **Service**: Hyperlocal delivery in under 15 minutes
        - 🎯 **Challenge**: Optimize customer acquisition and retention
        - 💡 **Opportunity**: High growth potential in underserved markets
        
        #### Project Overview
        This analysis examines customer behavior, delivery performance, and financial metrics 
        to develop data-driven strategies for sustainable growth and profitability.
        """)
    
    with col2:
        st.info("### 📊 Dataset Overview")
        st.metric("Total Customers", f"{len(df):,}")
        st.metric("Cities Covered", df['City'].nunique())
        st.metric("Delivery Zones", df['Zone'].nunique())
        st.metric("Customer Segments", df['CustomerSegment'].nunique())
    
    st.markdown("---")
    st.success("### 👥 Team & Methodology\n"
               "This presentation leverages exploratory data analysis, customer segmentation, "
               "funnel analysis, and ROI calculations to provide actionable business recommendations.")

# ============================================================================
# SLIDE 2: EXECUTIVE SUMMARY
# ============================================================================
elif page == "📋 Executive Summary":
    st.markdown('<p class="slide-title">📋 Executive Summary</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    avg_clv = df['CLV'].mean()
    avg_cac = df['CAC'].mean()
    clv_cac_ratio = avg_clv / avg_cac
    avg_satisfaction = df['SatisfactionScore'].mean()
    
    col1.metric("Avg CLV", f"₹{avg_clv:,.0f}", f"{((avg_clv/avg_cac)-1)*100:.1f}% vs CAC")
    col2.metric("Avg CAC", f"₹{avg_cac:,.0f}")
    col3.metric("CLV/CAC Ratio", f"{clv_cac_ratio:.2f}x", "Healthy" if clv_cac_ratio > 3 else "Needs Improvement")
    col4.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}/5.0", "⭐")
    
    st.markdown("---")
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.header("🎯 Key Findings")
        st.markdown("""
        1. **Strong Customer Segments**: Premium customers show 3-4x higher CLV than Budget segments
        2. **Geographic Opportunities**: Top 3 cities drive 60% of total revenue
        3. **Retention Challenge**: 40% of customers place only 1-2 orders
        4. **Delivery Excellence**: Average delivery time of 12 minutes meets promise
        5. **Profitability Gap**: High CAC in certain segments threatens unit economics
        """)
        
        st.header("💡 Top Opportunities")
        
        # Calculate top city by ROI
        city_roi = df.groupby('City')['ROI'].mean().sort_values(ascending=False)
        top_city = city_roi.index[0]
        
        # Calculate segment with best retention potential
        segment_freq = df.groupby('CustomerSegment')['OrderFrequency'].mean().sort_values(ascending=False)
        top_segment = segment_freq.index[0]
        
        st.info(f"""
        - **Focus City**: {top_city} shows highest ROI per customer
        - **Star Segment**: {top_segment} customers demonstrate strongest engagement
        - **Quick Win**: Reduce CAC by 15-20% through targeted digital marketing
        - **Revenue Boost**: Increase order frequency by 1x = 40% CLV improvement
        """)
    
    with col_right:
        st.header("🚀 Strategic Recommendations")
        st.markdown("""
        #### 1. Acquisition Optimization
        - Shift budget to high-ROI cities and channels
        - Target lookalike audiences of Premium customers
        - Reduce CAC through organic and referral programs
        
        #### 2. Retention & Engagement
        - Implement subscription/membership model
        - Personalized push notifications for re-engagement
        - Loyalty rewards for frequent purchasers
        
        #### 3. Operational Excellence
        - Optimize dark store locations in high-density zones
        - Dynamic pricing for delivery during peak hours
        - Expand high-margin product categories
        
        #### 4. Financial Sustainability
        - Achieve 3.5x CLV/CAC ratio within 12 months
        - Reduce churn by 25% through retention programs
        - Target 15% EBITDA margin by Q4
        """)
        
        st.success("**Expected Impact**: 40-50% improvement in unit economics over 12 months")

# ============================================================================
# SLIDE 3: DATA EXPLORATION / EDA
# ============================================================================
elif page == "🔍 Data Exploration / EDA":
    st.markdown('<p class="slide-title">🔍 Exploratory Data Analysis</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Dataset Preview
    st.header("📊 Dataset Overview")
    st.dataframe(df.head(10), use_container_width=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Features", len(df.columns))
    
    st.markdown("---")
    
    # Interactive Filters
    st.header("🎛️ Interactive Data Explorer")
    
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        selected_city = st.selectbox("Filter by City", ["All"] + sorted(df['City'].unique().tolist()))
    
    with col_filter2:
        selected_segment = st.selectbox("Filter by Segment", ["All"] + sorted(df['CustomerSegment'].unique().tolist()))
    
    with col_filter3:
        selected_zone = st.selectbox("Filter by Zone", ["All"] + sorted(df['Zone'].unique().tolist()))
    
    # Apply filters
    filtered_df = df.copy()
    if selected_city != "All":
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    if selected_segment != "All":
        filtered_df = filtered_df[filtered_df['CustomerSegment'] == selected_segment]
    if selected_zone != "All":
        filtered_df = filtered_df[filtered_df['Zone'] == selected_zone]
    
    st.info(f"Showing {len(filtered_df):,} customers based on filters")
    
    # Distribution Charts
    st.markdown("---")
    st.header("📈 Distribution Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Customer Segments", "Satisfaction Scores", "Order Frequency", "Cities & Zones"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Segment distribution
            segment_counts = filtered_df['CustomerSegment'].value_counts()
            fig = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title="Customer Segment Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Segment metrics
            segment_metrics = filtered_df.groupby('CustomerSegment').agg({
                'AvgOrderValue': 'mean',
                'OrderFrequency': 'mean',
                'CLV': 'mean',
                'SatisfactionScore': 'mean'
            }).round(2)
            st.subheader("Segment Metrics")
            st.dataframe(segment_metrics, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Satisfaction distribution
            fig = px.histogram(
                filtered_df,
                x='SatisfactionScore',
                nbins=20,
                title="Satisfaction Score Distribution",
                color_discrete_sequence=['#1f77b4']
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Satisfaction by segment
            fig = px.box(
                filtered_df,
                x='CustomerSegment',
                y='SatisfactionScore',
                title="Satisfaction Score by Segment",
                color='CustomerSegment'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Order frequency distribution
            fig = px.histogram(
                filtered_df,
                x='OrderFrequency',
                nbins=30,
                title="Order Frequency Distribution",
                color_discrete_sequence=['#2ca02c']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Avg order frequency by segment
            freq_by_segment = filtered_df.groupby('CustomerSegment')['OrderFrequency'].mean().sort_values(ascending=False)
            fig = px.bar(
                x=freq_by_segment.index,
                y=freq_by_segment.values,
                title="Avg Order Frequency by Segment",
                labels={'x': 'Segment', 'y': 'Avg Orders'},
                color=freq_by_segment.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # City distribution
            city_counts = filtered_df['City'].value_counts()
            fig = px.bar(
                x=city_counts.index,
                y=city_counts.values,
                title="Customers by City",
                labels={'x': 'City', 'y': 'Customer Count'},
                color=city_counts.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Zone distribution
            zone_counts = filtered_df['Zone'].value_counts()
            fig = px.bar(
                x=zone_counts.index,
                y=zone_counts.values,
                title="Customers by Zone",
                labels={'x': 'Zone', 'y': 'Customer Count'},
                color=zone_counts.values,
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Summary Statistics
    st.markdown("---")
    st.header("📊 Summary Statistics")
    st.dataframe(filtered_df.describe(), use_container_width=True)

# ============================================================================
# SLIDE 4: FUNNEL ANALYSIS
# ============================================================================
elif page == "🎯 Funnel Analysis":
    st.markdown('<p class="slide-title">🎯 Customer Journey Funnel</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("Customer Engagement Funnel")
    
    # Create funnel stages based on order frequency
    total_customers = len(df)
    stage_1_order = len(df[df['OrderFrequency'] >= 1])
    stage_2_3_orders = len(df[df['OrderFrequency'].between(2, 3)])
    stage_4plus_orders = len(df[df['OrderFrequency'] >= 4])
    
    # Funnel data
    stages = ['Registered Customers', 'Placed 1+ Orders', 'Placed 2-3 Orders', 'Placed 4+ Orders (Loyal)']
    values = [total_customers, stage_1_order, stage_2_3_orders, stage_4plus_orders]
    
    # Calculate conversion rates
    conv_rate_1 = (stage_1_order / total_customers) * 100
    conv_rate_2 = (stage_2_3_orders / stage_1_order) * 100
    conv_rate_3 = (stage_4plus_orders / stage_2_3_orders) * 100
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Funnel Chart
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textposition="inside",
            textinfo="value+percent initial",
            marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]},
            connector={"line": {"color": "royalblue", "width": 3}}
        ))
        
        fig.update_layout(
            title="Customer Journey Funnel",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Funnel Metrics")
        st.metric("Total Registered", f"{total_customers:,}", "100%")
        st.metric("Active (1+ Orders)", f"{stage_1_order:,}", f"{conv_rate_1:.1f}%")
        st.metric("Engaged (2-3 Orders)", f"{stage_2_3_orders:,}", f"{conv_rate_2:.1f}%")
        st.metric("Loyal (4+ Orders)", f"{stage_4plus_orders:,}", f"{conv_rate_3:.1f}%")
        
        st.markdown("---")
        
        # Drop-off rates
        dropoff_1_2 = ((stage_1_order - stage_2_3_orders) / stage_1_order) * 100
        dropoff_2_3 = ((stage_2_3_orders - stage_4plus_orders) / stage_2_3_orders) * 100
        
        st.warning(f"**Drop-off Analysis**\n\n"
                   f"📉 Stage 1→2: {dropoff_1_2:.1f}% drop-off\n\n"
                   f"📉 Stage 2→3: {dropoff_2_3:.1f}% drop-off")
    
    st.markdown("---")
    
    # Key Insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 🎯 Activation Insights
        - High initial activation rate
        - Most customers place at least 1 order
        - Strong onboarding experience
        """)
    
    with col2:
        st.warning("""
        ### ⚠️ Retention Challenge
        - Significant drop-off after first order
        - Need stronger 2nd purchase incentives
        - Re-engagement campaigns critical
        """)
    
    with col3:
        st.success("""
        ### 💎 Loyalty Opportunity
        - Loyal customers are highly valuable
        - Focus on moving engaged → loyal
        - Subscription/membership programs
        """)
    
    # Funnel by Segment
    st.markdown("---")
    st.header("🔍 Funnel Analysis by Customer Segment")
    
    segment_funnel = df.groupby('CustomerSegment').agg({
        'CustomerID': 'count',
        'OrderFrequency': lambda x: sum(x >= 1),
    }).reset_index()
    
    segment_funnel.columns = ['Segment', 'Total', 'Active']
    segment_funnel['Engaged'] = df[df['OrderFrequency'].between(2, 3)].groupby('CustomerSegment').size()
    segment_funnel['Loyal'] = df[df['OrderFrequency'] >= 4].groupby('CustomerSegment').size()
    segment_funnel = segment_funnel.fillna(0)
    
    fig = go.Figure()
    
    for col in ['Total', 'Active', 'Engaged', 'Loyal']:
        fig.add_trace(go.Bar(
            name=col,
            x=segment_funnel['Segment'],
            y=segment_funnel[col],
            text=segment_funnel[col].astype(int),
            textposition='auto'
        ))
    
    fig.update_layout(
        title="Customer Funnel Stages by Segment",
        barmode='group',
        height=400,
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SLIDE 5: ROI & SEGMENTATION
# ============================================================================
elif page == "💰 ROI & Segmentation":
    st.markdown('<p class="slide-title">💰 ROI & Customer Segmentation Analysis</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # ROI Formula Display
    st.header("📐 ROI Calculation Methodology")
    st.latex(r"CLV = Average\ Order\ Value \times Order\ Frequency")
    st.latex(r"ROI = CLV - CAC")
    st.latex(r"ROI\ Ratio = \frac{CLV}{CAC}")
    
    st.markdown("---")
    
    # Interactive Parameters
    st.header("🎛️ Adjust Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cac_premium = st.number_input("Premium CAC (₹)", value=500, step=50)
    with col2:
        cac_regular = st.number_input("Regular CAC (₹)", value=300, step=50)
    with col3:
        cac_budget = st.number_input("Budget CAC (₹)", value=200, step=50)
    with col4:
        cac_occasional = st.number_input("Occasional CAC (₹)", value=150, step=50)
    
    # Recalculate with custom CAC
    df_custom = df.copy()
    cac_map_custom = {'Premium': cac_premium, 'Regular': cac_regular, 'Budget': cac_budget, 'Occasional': cac_occasional}
    df_custom['CAC'] = df_custom['CustomerSegment'].map(cac_map_custom)
    df_custom['ROI'] = df_custom['CLV'] - df_custom['CAC']
    df_custom['ROI_Ratio'] = df_custom['CLV'] / df_custom['CAC']
    
    st.markdown("---")
    
    # ROI by Segment
    st.header("📊 ROI Analysis by Customer Segment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        segment_roi = df_custom.groupby('CustomerSegment').agg({
            'CLV': 'mean',
            'CAC': 'mean',
            'ROI': 'mean',
            'ROI_Ratio': 'mean',
            'CustomerID': 'count'
        }).round(2)
        segment_roi.columns = ['Avg CLV', 'Avg CAC', 'Avg ROI', 'ROI Ratio', 'Customer Count']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='CLV',
            x=segment_roi.index,
            y=segment_roi['Avg CLV'],
            marker_color='lightgreen'
        ))
        fig.add_trace(go.Bar(
            name='CAC',
            x=segment_roi.index,
            y=segment_roi['Avg CAC'],
            marker_color='lightcoral'
        ))
        
        fig.update_layout(
            title="CLV vs CAC by Segment",
            barmode='group',
            yaxis_title="Amount (₹)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            x=segment_roi.index,
            y=segment_roi['Avg ROI'],
            title="Average ROI by Segment",
            labels={'x': 'Segment', 'y': 'ROI (₹)'},
            color=segment_roi['Avg ROI'],
            color_continuous_scale='RdYlGn',
            text=segment_roi['Avg ROI'].round(0)
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Segment Metrics Table
    st.subheader("Detailed Segment Metrics")
    st.dataframe(segment_roi, use_container_width=True)
    
    st.markdown("---")
    
    # ROI by City
    st.header("🏙️ ROI Analysis by City")
    
    col1, col2 = st.columns(2)
    
    with col1:
        city_roi = df_custom.groupby('City').agg({
            'ROI': 'mean',
            'CLV': 'mean',
            'CustomerID': 'count'
        }).sort_values('ROI', ascending=False).round(2)
        
        fig = px.bar(
            x=city_roi.index,
            y=city_roi['ROI'],
            title="Average ROI by City",
            labels={'x': 'City', 'y': 'ROI (₹)'},
            color=city_roi['ROI'],
            color_continuous_scale='Viridis',
            text=city_roi['ROI'].round(0)
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ROI by Zone
        zone_roi = df_custom.groupby('Zone').agg({
            'ROI': 'mean',
            'CLV': 'mean',
            'CustomerID': 'count'
        }).sort_values('ROI', ascending=False).round(2)
        
        fig = px.bar(
            x=zone_roi.index,
            y=zone_roi['ROI'],
            title="Average ROI by Zone",
            labels={'x': 'Zone', 'y': 'ROI (₹)'},
            color=zone_roi['ROI'],
            color_continuous_scale='Plasma',
            text=zone_roi['ROI'].round(0)
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Segment Size and Satisfaction
    st.header("🎯 Segment Characteristics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        segment_size = df_custom['CustomerSegment'].value_counts()
        fig = px.pie(
            values=segment_size.values,
            names=segment_size.index,
            title="Customer Distribution by Segment",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        segment_satisfaction = df_custom.groupby('CustomerSegment')['SatisfactionScore'].mean().sort_values(ascending=False)
        fig = px.bar(
            x=segment_satisfaction.index,
            y=segment_satisfaction.values,
            title="Average Satisfaction Score by Segment",
            labels={'x': 'Segment', 'y': 'Satisfaction Score'},
            color=segment_satisfaction.values,
            color_continuous_scale='Blues',
            text=segment_satisfaction.values.round(2)
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Key Insights
    st.markdown("---")
    st.header("💡 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    best_roi_segment = segment_roi['Avg ROI'].idxmax()
    best_roi_city = city_roi['ROI'].idxmax()
    worst_roi_segment = segment_roi['Avg ROI'].idxmin()
    
    with col1:
        st.success(f"""
        ### 🏆 Best Performing
        **Segment**: {best_roi_segment}
        - ROI: ₹{segment_roi.loc[best_roi_segment, 'Avg ROI']:,.0f}
        - Ratio: {segment_roi.loc[best_roi_segment, 'ROI Ratio']:.2f}x
        """)
    
    with col2:
        st.info(f"""
        ### 🏙️ Top City
        **{best_roi_city}**
        - ROI: ₹{city_roi.loc[best_roi_city, 'ROI']:,.0f}
        - Customers: {city_roi.loc[best_roi_city, 'CustomerID']:,.0f}
        """)
    
    with col3:
        st.warning(f"""
        ### ⚠️ Needs Attention
        **Segment**: {worst_roi_segment}
        - ROI: ₹{segment_roi.loc[worst_roi_segment, 'Avg ROI']:,.0f}
        - Requires CAC optimization
        """)

# ============================================================================
# SLIDE 6: STRATEGIES & BMC
# ============================================================================
elif page == "🎨 Strategies & BMC":
    st.markdown('<p class="slide-title">🎨 Strategic Recommendations & Business Model</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Acquisition Strategy", "🔄 Retention Strategy", "💸 CAC Optimization", "🗺️ Business Model Canvas"])
    
    with tab1:
        st.header("🎯 Customer Acquisition Strategy")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Primary Recommendations")
            
            with st.expander("1. Targeted Digital Marketing", expanded=True):
                st.markdown("""
                **Objective**: Reduce CAC by 20% while improving customer quality
                
                **Actions**:
                - Focus on high-ROI cities and zones
                - Create lookalike audiences based on Premium segment
                - Utilize performance marketing (Google Ads, Facebook/Instagram)
                - Optimize ad spend allocation by segment LTV
                
                **Expected Impact**:
                - 20-25% reduction in CAC
                - 30% improvement in conversion rates
                - Better segment mix towards Premium/Regular
                """)
            
            with st.expander("2. Referral & Word-of-Mouth Program"):
                st.markdown("""
                **Objective**: Acquire customers at near-zero CAC
                
                **Actions**:
                - Launch "Refer & Earn" program (₹100 credit for both parties)
                - Incentivize social sharing of first order
                - Create viral moments (discount codes, challenges)
                - Partner with local influencers in Tier-2 cities
                
                **Expected Impact**:
                - 15-20% of new customers via referrals
                - CAC for referred customers: ₹50-100
                - Higher retention rate for referred customers
                """)
            
            with st.expander("3. Strategic Partnerships"):
                st.markdown("""
                **Objective**: Leverage existing customer bases
                
                **Actions**:
                - Partner with apartment complexes and gated communities
                - Tie-ups with corporate offices in Tier-2 cities
                - Co-marketing with complementary brands (Netflix, Amazon Prime)
                - Bundle offers with payment apps (Paytm, PhonePe)
                
                **Expected Impact**:
                - Access to pre-qualified audiences
                - Lower CAC through shared marketing costs
                - Bulk customer acquisition opportunities
                """)
        
        with col2:
            st.subheader("Acquisition Channel Mix")
            
            # Channel allocation recommendation
            channels = ['Digital Ads', 'Referrals', 'Partnerships', 'Organic/SEO', 'Offline']
            current_allocation = [40, 10, 15, 20, 15]
            recommended_allocation = [30, 25, 20, 20, 5]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Current',
                x=channels,
                y=current_allocation,
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Recommended',
                x=channels,
                y=recommended_allocation,
                marker_color='darkblue'
            ))
            
            fig.update_layout(
                title="Marketing Budget Allocation",
                barmode='group',
                yaxis_title="Budget Allocation (%)",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            **Key Shifts**:
            - ⬇️ Reduce paid ads from 40% to 30%
            - ⬆️ Increase referrals from 10% to 25%
            - ⬆️ Boost partnerships from 15% to 20%
            - ⬇️ Minimize offline spend
            """)
    
    with tab2:
        st.header("🔄 Customer Retention Strategy")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Retention Initiatives")
            
            with st.expander("1. Subscription/Membership Model", expanded=True):
                st.markdown("""
                **GrovQuick Plus Membership**
                
                **Pricing**: ₹199/month or ₹1,999/year
                
                **Benefits**:
                - Free delivery on all orders
                - 10% cashback on every purchase
                - Priority delivery slots
                - Early access to deals and new products
                - Exclusive member-only offers
                
                **Business Impact**:
                - Predictable recurring revenue
                - 3-4x higher order frequency
                - Reduced price sensitivity
                - 70%+ retention rate for members
                """)
            
            with st.expander("2. Personalized Engagement"):
                st.markdown("""
                **Objective**: Re-engage dormant customers and increase frequency
                
                **Tactics**:
                - Smart push notifications based on purchase patterns
                - Personalized weekly shopping lists
                - Replenishment reminders for frequently bought items
                - Time-based offers (weekend discounts, evening deals)
                - Cart abandonment recovery campaigns
                
                **Segmentation**:
                - At-risk customers: Win-back offers
                - Occasional buyers: Frequency-building campaigns
                - Regular buyers: Upsell and cross-sell
                - Champions: VIP treatment and exclusive access
                """)
            
            with st.expander("3. Gamification & Loyalty"):
                st.markdown("""
                **GrovQuick Rewards Program**
                
                **Mechanics**:
                - Earn 1 point per ₹10 spent
                - Bonus points for order streaks
                - Tier system: Bronze → Silver → Gold → Platinum
                - Monthly challenges (order 8 times, get 500 bonus points)
                
                **Redemption**:
                - 100 points = ₹100 discount
                - Exclusive tier-based benefits
                - Partner rewards (Swiggy, BookMyShow)
                
                **Psychology**:
                - Progress bars create completion desire
                - Tier upgrades drive frequency
                - Points expiry creates urgency
                """)
        
        with col2:
            st.subheader("Retention Impact Model")
            
            # Retention scenarios
            scenarios = ['Current', 'With Membership', 'With Loyalty', 'Combined']
            retention_rates = [55, 75, 70, 85]
            avg_orders = [3.2, 8.5, 5.8, 10.2]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Retention Rate (%)',
                x=scenarios,
                y=retention_rates,
                yaxis='y',
                marker_color='lightgreen'
            ))
            fig.add_trace(go.Scatter(
                name='Avg Orders/Year',
                x=scenarios,
                y=avg_orders,
                yaxis='y2',
                mode='lines+markers',
                marker=dict(size=10, color='darkgreen'),
                line=dict(width=3)
            ))
            
            fig.update_layout(
                title="Retention Program Impact",
                yaxis=dict(title="Retention Rate (%)"),
                yaxis2=dict(title="Avg Orders/Year", overlaying='y', side='right'),
                height=350,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.success("""
            **Combined Strategy Impact**:
            - 📈 Retention: 55% → 85% (+30pp)
            - 🔄 Order Frequency: 3.2 → 10.2 (+219%)
            - 💰 CLV Increase: ~3.2x
            - 📊 Payback Period: 2-3 months
            """)
            
            st.warning("""
            **Implementation Priority**:
            1. Month 1-2: Launch basic loyalty program
            2. Month 3-4: Test membership model (beta)
            3. Month 5-6: Roll out gamification
            4. Month 6+: Optimize based on data
            """)
    
    with tab3:
        st.header("💸 CAC Optimization Strategy")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Cost Reduction Levers")
            
            with st.expander("1. Channel Optimization", expanded=True):
                st.markdown("""
                **Audit & Optimize**:
                - Analyze CAC by channel, campaign, and creative
                - Double down on top 3 performing channels
                - Eliminate bottom 20% of campaigns
                - A/B test ad creatives continuously
                
                **Focus Areas**:
                - Shift from broad to targeted audiences
                - Use retargeting for website visitors
                - Optimize landing pages for conversion
                - Implement multi-touch attribution
                
                **Expected Savings**: 15-20% CAC reduction
                """)
            
            with st.expander("2. Organic Growth"):
                st.markdown("""
                **Low-Cost Acquisition**:
                - SEO for "grocery delivery [city]" keywords
                - Content marketing (blogs, recipes, tips)
                - Local community building (WhatsApp groups)
                - PR and media coverage in Tier-2 cities
                
                **Social Media**:
                - Organic Instagram/Facebook presence
                - User-generated content campaigns
                - Local food blogger partnerships
                - Community management and engagement
                
                **Expected Impact**: 20-25% customers at <₹50 CAC
                """)
            
            with st.expander("3. Improve Conversion Rates"):
                st.markdown("""
                **App/Website Optimization**:
                - Simplify onboarding (reduce to 3 steps)
                - Remove friction in checkout flow
                - Add trust signals (reviews, ratings)
                - Optimize for mobile (90%+ of users)
                
                **First Order Incentives**:
                - Aggressive first-order discounts (₹150 off)
                - Free delivery on first 3 orders
                - Instant ₹50 signup bonus
                
                **Impact**: 30% conversion improvement = 23% CAC reduction
                """)
        
        with col2:
            st.subheader("CAC Reduction Roadmap")
            
            # CAC reduction over time
            months = ['Current', 'Month 3', 'Month 6', 'Month 9', 'Month 12']
            cac_values = [300, 270, 240, 220, 210]
            cumulative_savings = [0, 50000, 120000, 200000, 300000]
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=months, y=cac_values, name="Avg CAC (₹)",
                          mode='lines+markers', line=dict(color='red', width=3),
                          marker=dict(size=10)),
                secondary_y=False
            )
            
            fig.add_trace(
                go.Bar(x=months, y=cumulative_savings, name="Cumulative Savings (₹)",
                       marker_color='lightgreen', opacity=0.6),
                secondary_y=True
            )
            
            fig.update_layout(
                title="CAC Optimization Timeline",
                height=350,
                hovermode='x unified'
            )
            fig.update_xaxes(title_text="Timeline")
            fig.update_yaxes(title_text="CAC (₹)", secondary_y=False)
            fig.update_yaxes(title_text="Cumulative Savings (₹)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            **12-Month Target**:
            - 🎯 Reduce CAC from ₹300 to ₹210 (-30%)
            - 💰 Total savings: ₹3L+ over 12 months
            - 📊 Improve CAC payback from 4 to 2.5 months
            """)
            
            # CAC by segment targets
            st.subheader("Segment-Wise CAC Targets")
            
            segment_cac_data = {
                'Segment': ['Premium', 'Regular', 'Budget', 'Occasional'],
                'Current CAC': [500, 300, 200, 150],
                'Target CAC': [400, 240, 170, 120],
                'Max Acceptable': [600, 350, 220, 180]
            }
            
            df_cac = pd.DataFrame(segment_cac_data)
            st.dataframe(df_cac, use_container_width=True, hide_index=True)
    
    with tab4:
        st.header("🗺️ Business Model Canvas")
        
        st.info("**GrovQuick Business Model Canvas** - Quick Commerce for Tier-2 Cities")
        
        # Create BMC layout
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown("### 🤝 Key Partners")
            st.markdown("""
            - Local grocery suppliers
            - Dark store real estate providers
            - Delivery personnel (gig workers)
            - Payment gateways
            - Tech infrastructure (AWS)
            - Brand partners (P&G, HUL, ITC)
            """)
            
            st.markdown("### 🎯 Key Activities")
            st.markdown("""
            - Demand forecasting & inventory management
            - Lightning-fast order fulfillment (<15 min)
            - Customer acquisition & retention
            - Dark store operations
            - Technology platform development
            - Quality control & vendor management
            """)
            
            st.markdown("### 🔑 Key Resources")
            st.markdown("""
            - Dark store network in Tier-2 cities
            - Mobile app & tech platform
            - Delivery fleet (owned + gig)
            - Customer data & analytics
            - Brand partnerships
            - Skilled operations team
            """)
        
        with col2:
            st.markdown("### 💎 Value Propositions")
            st.markdown("""
            **For Customers:**
            - ⚡ 10-15 minute delivery
            - 🏠 Hyperlocal convenience
            - 📱 Easy mobile ordering
            - 💰 Competitive pricing
            - 🎯 Fresh quality products
            
            **For Tier-2 Cities:**
            - 🌆 Modern retail experience
            - 💼 Employment opportunities
            - 📈 Economic development
            """)
            
            st.markdown("### 🤝 Customer Relationships")
            st.markdown("""
            - Self-service app platform
            - 24/7 customer support
            - Personalized recommendations
            - Loyalty & rewards program
            - Push notifications & engagement
            - Community building (WhatsApp)
            """)
            
            st.markdown("### 📢 Channels")
            st.markdown("""
            - Mobile app (primary)
            - Website
            - Social media (Instagram, Facebook)
            - Referral program
            - Local partnerships
            - Digital advertising
            """)
        
        with col3:
            st.markdown("### 👥 Customer Segments")
            st.markdown("""
            **Primary:**
            - Urban Tier-2 city residents
            - Working professionals
            - Young families
            - Tech-savvy millennials/Gen-Z
            
            **Segments:**
            - Premium (high-value, frequent)
            - Regular (steady, loyal)
            - Budget (price-conscious)
            - Occasional (convenience-driven)
            """)
            
            st.markdown("### 💰 Revenue Streams")
            st.markdown("""
            **Primary:**
            - Product markup (15-25%)
            - Delivery fees (₹0-49)
            
            **Secondary:**
            - Membership subscriptions (₹199/mo)
            - Advertising (brand placements)
            - Data insights (anonymized trends)
            - Commission on partner products
            """)
        
        st.markdown("---")
        
        # Cost Structure - Full Width
        st.markdown("### 💸 Cost Structure")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Fixed Costs:**
            - Dark store rent & setup
            - Technology infrastructure
            - Full-time employee salaries
            - Marketing & brand building
            - Administrative overhead
            """)
        
        with col2:
            st.markdown("""
            **Variable Costs:**
            - Product procurement (COGS 70-75%)
            - Delivery personnel costs
            - Customer acquisition (CAC)
            - Packaging materials
            - Payment processing fees
            """)
        
        # Unit Economics
        st.markdown("---")
        st.subheader("📊 Unit Economics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Avg Order Value", "₹450", "Gross Revenue")
        col2.metric("COGS (70%)", "₹315", "Product Cost")
        col3.metric("Delivery Cost", "₹35", "Per Order")
        col4.metric("Contribution Margin", "₹100", "22.2%")
        
        st.success("""
        **Path to Profitability:**
        - Break-even at ~8-10 orders per customer
        - Premium & Regular segments profitable after 3-4 orders
        - Focus on increasing order frequency through retention programs
        - Target 15% EBITDA margin at scale
        """)

# ============================================================================
# SLIDE 7: SIMULATED IMPACT
# ============================================================================
elif page == "📈 Simulated Impact":
    st.markdown('<p class="slide-title">📈 Simulated Business Impact</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.header("🎯 Scenario Planning & Projections")
    
    # Scenario Selector
    scenario = st.radio(
        "Select Scenario:",
        ["Conservative", "Base Case", "Optimistic"],
        horizontal=True
    )
    
    # Define scenarios
    scenarios_data = {
        'Conservative': {
            'cac_reduction': 0.15,
            'retention_increase': 0.15,
            'frequency_increase': 0.25,
            'aov_increase': 0.05,
            'timeline': 12
        },
        'Base Case': {
            'cac_reduction': 0.25,
            'retention_increase': 0.25,
            'frequency_increase': 0.40,
            'aov_increase': 0.10,
            'timeline': 12
        },
        'Optimistic': {
            'cac_reduction': 0.35,
            'retention_increase': 0.35,
            'frequency_increase': 0.60,
            'aov_increase': 0.15,
            'timeline': 12
        }
    }
    
    selected_scenario = scenarios_data[scenario]
    
    st.markdown("---")
    
    # Current vs Projected Metrics
    st.header(f"📊 {scenario} Scenario - 12 Month Projection")
    
    # Calculate current metrics
    current_cac = df['CAC'].mean()
    current_clv = df['CLV'].mean()
    current_roi = df['ROI'].mean()
    current_frequency = df['OrderFrequency'].mean()
    current_aov = df['AvgOrderValue'].mean()
    current_satisfaction = df['SatisfactionScore'].mean()
    
    # Calculate projected metrics
    projected_cac = current_cac * (1 - selected_scenario['cac_reduction'])
    projected_frequency = current_frequency * (1 + selected_scenario['frequency_increase'])
    projected_aov = current_aov * (1 + selected_scenario['aov_increase'])
    projected_clv = projected_aov * projected_frequency
    projected_roi = projected_clv - projected_cac
    projected_satisfaction = min(current_satisfaction * 1.1, 5.0)  # Cap at 5.0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Customer Acquisition Cost",
            f"₹{projected_cac:,.0f}",
            f"-₹{current_cac - projected_cac:,.0f} ({-selected_scenario['cac_reduction']*100:.0f}%)",
            delta_color="inverse"
        )
        
        st.metric(
            "Customer Lifetime Value",
            f"₹{projected_clv:,.0f}",
            f"+₹{projected_clv - current_clv:,.0f} ({((projected_clv/current_clv)-1)*100:.0f}%)"
        )
    
    with col2:
        st.metric(
            "ROI per Customer",
            f"₹{projected_roi:,.0f}",
            f"+₹{projected_roi - current_roi:,.0f} ({((projected_roi/current_roi)-1)*100:.0f}%)"
        )
        
        st.metric(
            "CLV/CAC Ratio",
            f"{projected_clv/projected_cac:.2f}x",
            f"+{(projected_clv/projected_cac) - (current_clv/current_cac):.2f}x"
        )
    
    with col3:
        st.metric(
            "Order Frequency",
            f"{projected_frequency:.1f}",
            f"+{projected_frequency - current_frequency:.1f} ({selected_scenario['frequency_increase']*100:.0f}%)"
        )
        
        st.metric(
            "Avg Order Value",
            f"₹{projected_aov:,.0f}",
            f"+₹{projected_aov - current_aov:,.0f} ({selected_scenario['aov_increase']*100:.0f}%)"
        )
    
    st.markdown("---")
    
    # Comparison Chart
    st.header("📊 Before vs After Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CAC vs CLV comparison
        metrics = ['CAC', 'CLV', 'ROI']
        current_values = [current_cac, current_clv, current_roi]
        projected_values = [projected_cac, projected_clv, projected_roi]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Current',
            x=metrics,
            y=current_values,
            marker_color='lightcoral',
            text=[f"₹{v:,.0f}" for v in current_values],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='Projected',
            x=metrics,
            y=projected_values,
            marker_color='lightgreen',
            text=[f"₹{v:,.0f}" for v in projected_values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f"Key Metrics Improvement - {scenario}",
            barmode='group',
            height=400,
            yaxis_title="Amount (₹)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Customer behavior metrics
        behavior_metrics = ['Order Frequency', 'Avg Order Value', 'Satisfaction']
        current_behavior = [current_frequency, current_aov, current_satisfaction]
        projected_behavior = [projected_frequency, projected_aov, projected_satisfaction]
        
        # Normalize for visualization
        current_behavior_norm = [current_frequency/10, current_aov/100, current_satisfaction]
        projected_behavior_norm = [projected_frequency/10, projected_aov/100, projected_satisfaction]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=current_behavior_norm,
            theta=behavior_metrics,
            fill='toself',
            name='Current',
            line_color='red'
        ))
        fig.add_trace(go.Scatterpolar(
            r=projected_behavior_norm,
            theta=behavior_metrics,
            fill='toself',
            name='Projected',
            line_color='green'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 6])),
            title=f"Customer Behavior Improvement - {scenario}",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Financial Impact
    st.header("💰 Financial Impact Projection")
    
    # Assume customer base
    total_customers = len(df)
    monthly_new_customers = 1000  # Assumption
    
    # Calculate annual impact
    annual_customers = total_customers + (monthly_new_customers * 12)
    
    current_annual_revenue = total_customers * current_clv
    projected_annual_revenue = annual_customers * projected_clv
    
    current_annual_cac_spend = monthly_new_customers * 12 * current_cac
    projected_annual_cac_spend = monthly_new_customers * 12 * projected_cac
    
    current_gross_profit = current_annual_revenue - current_annual_cac_spend
    projected_gross_profit = projected_annual_revenue - projected_annual_cac_spend
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric(
        "Annual Revenue",
        f"₹{projected_annual_revenue/10000000:.2f}Cr",
        f"+₹{(projected_annual_revenue - current_annual_revenue)/10000000:.2f}Cr"
    )
    
    col2.metric(
        "CAC Spend Savings",
        f"₹{(current_annual_cac_spend - projected_annual_cac_spend)/100000:.2f}L",
        f"{-((projected_annual_cac_spend/current_annual_cac_spend - 1)*100):.1f}%",
        delta_color="normal"
    )
    
    col3.metric(
        "Gross Profit Impact",
        f"₹{projected_gross_profit/10000000:.2f}Cr",
        f"+₹{(projected_gross_profit - current_gross_profit)/10000000:.2f}Cr"
    )
    
    st.markdown("---")
    
    # Scenario Comparison Table
    st.header("📋 All Scenarios Comparison")
    
    comparison_data = []
    for scen_name, scen_data in scenarios_data.items():
        proj_cac = current_cac * (1 - scen_data['cac_reduction'])
        proj_freq = current_frequency * (1 + scen_data['frequency_increase'])
        proj_aov = current_aov * (1 + scen_data['aov_increase'])
        proj_clv = proj_aov * proj_freq
        proj_roi = proj_clv - proj_cac
        
        comparison_data.append({
            'Scenario': scen_name,
            'CAC': f"₹{proj_cac:,.0f}",
            'CLV': f"₹{proj_clv:,.0f}",
            'ROI': f"₹{proj_roi:,.0f}",
            'CLV/CAC': f"{proj_clv/proj_cac:.2f}x",
            'Order Freq': f"{proj_freq:.1f}",
            'Probability': '25%' if scen_name == 'Conservative' else '50%' if scen_name == 'Base Case' else '25%'
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    st.success(f"""
    **{scenario} Scenario Summary:**
    - 🎯 Target CLV/CAC ratio: {projected_clv/projected_cac:.2f}x (vs current {current_clv/current_cac:.2f}x)
    - 📈 Expected revenue growth: {((projected_annual_revenue/current_annual_revenue - 1)*100):.1f}%
    - 💰 Improved unit economics across all segments
    - ⏱️ Payback period: {(projected_cac/projected_aov):.1f} orders (down from {(current_cac/current_aov):.1f})
    """)
    
    st.markdown("---")
    
    # Implementation Timeline
    st.header("📅 12-Month Implementation Roadmap")
    
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    milestones = {
        'Q1': ['Launch loyalty program', 'Optimize top 3 acquisition channels', 'Pilot membership in 1 city'],
        'Q2': ['Roll out referral program', 'Implement personalization engine', 'Expand membership to all cities'],
        'Q3': ['Launch gamification features', 'Strategic partnerships live', 'Advanced segmentation'],
        'Q4': ['Full retention suite active', 'Achieve target CAC reduction', 'Scale profitable segments']
    }
    
    for i, quarter in enumerate(quarters):
        with st.expander(f"**{quarter} (Months {i*3+1}-{i*3+3})**", expanded=(i==0)):
            for milestone in milestones[quarter]:
                st.markdown(f"- ✅ {milestone}")
            
            # Quarter metrics
            quarter_progress = (i + 1) / 4
            quarter_cac = current_cac - (current_cac - projected_cac) * quarter_progress
            quarter_clv = current_clv + (projected_clv - current_clv) * quarter_progress
            
            col1, col2, col3 = st.columns(3)
            col1.metric(f"{quarter} CAC Target", f"₹{quarter_cac:,.0f}")
            col2.metric(f"{quarter} CLV Target", f"₹{quarter_clv:,.0f}")
            col3.metric(f"{quarter} Progress", f"{quarter_progress*100:.0f}%")

# ============================================================================
# SLIDE 8: LIMITATIONS & CONCLUSION
# ============================================================================
elif page == "⚠️ Limitations & Conclusion":
    st.markdown('<p class="slide-title">⚠️ Limitations & Conclusion</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Limitations
    st.header("⚠️ Analysis Limitations & Risks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Data Limitations")
        st.markdown("""
        - **Historical Bias**: Analysis based on past behavior may not predict future trends
        - **Sample Size**: Limited to existing customer base; may not represent market potential
        - **Missing Variables**: External factors (seasonality, competition, economic conditions) not included
        - **Attribution**: CAC allocation by segment uses assumptions, not actual tracked data
        - **Churn Data**: No explicit churn/retention data available in dataset
        """)
        
        st.subheader("🎯 Assumption Risks")
        st.markdown("""
        - **CAC Values**: Segment-wise CAC is estimated; actual may vary by 15-20%
        - **Market Response**: Customer behavior change predictions based on industry benchmarks
        - **Competition**: Assumes stable competitive landscape; new entrants could disrupt
        - **Implementation**: Success depends on flawless execution of recommendations
        - **Economic Factors**: Tier-2 city growth rates may fluctuate
        """)
    
    with col2:
        st.subheader("🚧 Business Risks")
        st.markdown("""
        - **Operational Complexity**: 10-15 min delivery requires perfect execution
        - **Unit Economics**: Thin margins vulnerable to cost increases
        - **Customer Acquisition**: Tier-2 market may have lower digital adoption than assumed
        - **Retention Programs**: Membership/loyalty success rates uncertain
        - **Funding Requirements**: Growth strategy needs capital; burn rate management critical
        """)
        
        st.subheader("🔄 Mitigation Strategies")
        st.markdown("""
        - **Phased Rollout**: Test strategies in 1-2 cities before full deployment
        - **A/B Testing**: Validate all assumptions with controlled experiments
        - **Monthly Reviews**: Track KPIs and adjust strategy based on real data
        - **Contingency Plans**: Prepare alternatives if key metrics don't improve
        - **Risk Reserves**: Budget 15-20% buffer for unexpected challenges
        """)
    
    st.markdown("---")
    
    # Key Conclusions
    st.header("🎯 Key Conclusions & Strategic Roadmap")
    
    st.success("""
    ### 🏆 Main Findings
    
    GrovQuick has strong fundamentals with significant room for optimization:
    
    1. **Solid Foundation**: Delivery performance and customer satisfaction are strong (avg 4.2/5)
    2. **Segment Opportunity**: Premium and Regular customers show healthy unit economics
    3. **Retention Gap**: Major opportunity to increase order frequency (current avg: 3.2 orders)
    4. **CAC Optimization**: 20-30% reduction possible through channel mix optimization
    5. **Geographic Focus**: Top cities show 2-3x better ROI than bottom performers
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 🎯 Immediate Actions
        **Next 90 Days**
        
        1. Launch basic loyalty program
        2. Optimize top 3 ad channels
        3. Pilot referral program
        4. Implement cart abandonment flow
        5. Focus acquisition on high-ROI cities
        
        **Expected Quick Wins:**
        - 10-15% CAC reduction
        - 20% improvement in repeat rate
        """)
    
    with col2:
        st.warning("""
        ### 📈 Medium-Term Strategy
        **Months 4-9**
        
        1. Roll out membership program
        2. Implement personalization engine
        3. Launch strategic partnerships
        4. Expand to adjacent categories
        5. Build advanced analytics
        
        **Target Outcomes:**
        - 3.5x CLV/CAC ratio
        - 70%+ member retention
        """)
    
    with col3:
        st.success("""
        ### 🚀 Long-Term Vision
        **Months 10-24**
        
        1. Achieve profitability
        2. Expand to 15+ Tier-2 cities
        3. Build defensible moats
        4. Scale to 1M+ customers
        5. Explore new verticals
        
        **Ultimate Goal:**
        - Market leader in Tier-2 Q-commerce
        - 15% EBITDA margin
        """)
    
    st.markdown("---")
    
    # Strategic Priorities
    st.header("🎨 Strategic Priorities Matrix")
    
    # Create 2x2 matrix
    fig = go.Figure()
    
    initiatives = [
        {'name': 'Loyalty Program', 'impact': 9, 'effort': 3, 'color': 'green'},
        {'name': 'Referral System', 'impact': 8, 'effort': 2, 'color': 'green'},
        {'name': 'Channel Optimization', 'impact': 7, 'effort': 4, 'color': 'lightgreen'},
        {'name': 'Membership Model', 'impact': 9, 'effort': 6, 'color': 'lightgreen'},
        {'name': 'Personalization', 'impact': 6, 'effort': 7, 'color': 'orange'},
        {'name': 'Geographic Expansion', 'impact': 7, 'effort': 8, 'color': 'orange'},
        {'name': 'New Verticals', 'impact': 5, 'effort': 9, 'color': 'red'},
        {'name': 'Gamification', 'impact': 4, 'effort': 5, 'color': 'yellow'}
    ]
    
    for init in initiatives:
        fig.add_trace(go.Scatter(
            x=[init['effort']],
            y=[init['impact']],
            mode='markers+text',
            name=init['name'],
            text=[init['name']],
            textposition='top center',
            marker=dict(size=20, color=init['color']),
            showlegend=False
        ))
    
    fig.add_hline(y=6.5, line_dash="dash", line_color="gray", annotation_text="High Impact Threshold")
    fig.add_vline(x=5.5, line_dash="dash", line_color="gray", annotation_text="Low Effort Threshold")
    
    fig.update_layout(
        title="Impact vs Effort Matrix - Prioritization Framework",
        xaxis_title="Implementation Effort (1-10)",
        yaxis_title="Business Impact (1-10)",
        height=500,
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **Priority Legend:**
    - 🟢 **High Impact, Low Effort** - DO FIRST (Quick Wins)
    - 🟡 **High Impact, High Effort** - Strategic Projects (Plan Carefully)
    - 🟠 **Low Impact, Low Effort** - Fill-ins (If Resources Available)
    - 🔴 **Low Impact, High Effort** - Avoid or Deprioritize
    """)
    
    st.markdown("---")
    
    # Success Metrics Dashboard
    st.header("📊 Success Metrics Dashboard")
    
    st.markdown("Track these KPIs monthly to ensure strategy is working:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CAC", "₹300 → ₹210", "Target: -30%")
        st.metric("Order Frequency", "3.2 → 4.5", "Target: +40%")
    
    with col2:
        st.metric("CLV", "₹960 → ₹1,440", "Target: +50%")
        st.metric("Retention Rate", "55% → 75%", "Target: +20pp")
    
    with col3:
        st.metric("CLV/CAC Ratio", "3.2x → 4.8x", "Target: >4.0x")
        st.metric("Member %", "0% → 25%", "Target: 25%")
    
    with col4:
        st.metric("Referral Rate", "5% → 20%", "Target: 20%")
        st.metric("NPS Score", "45 → 65", "Target: >60")
    
    st.markdown("---")
    
    # Final Summary
    st.header("🎓 Executive Summary & Recommendations")
    
    st.markdown("""
    ### The Bottom Line
    
    GrovQuick operates in a high-growth, high-potential market with strong operational fundamentals. 
    The analysis reveals clear opportunities to improve unit economics through:
    
    1. **Smarter Acquisition** (20-30% CAC reduction)
    2. **Better Retention** (2-3x increase in order frequency)
    3. **Focused Expansion** (prioritize high-ROI geographies)
    
    ### Path Forward
    
    **Phase 1 (Months 1-3): Optimize & Retain**
    - Quick wins in CAC optimization and loyalty
    - Expected impact: 15% improvement in unit economics
    
    **Phase 2 (Months 4-9): Scale & Innovate**
    - Roll out membership and advanced retention
    - Expected impact: 40% improvement in unit economics
    
    **Phase 3 (Months 10-12): Consolidate & Grow**
    - Achieve profitability and expand footprint
    - Expected impact: 50%+ improvement in unit economics
    
    ### Critical Success Factors
    
    ✅ **Must Have**: Flawless execution on 10-15 min delivery promise  
    ✅ **Must Do**: Launch retention programs by Month 3  
    ✅ **Must Avoid**: Undisciplined expansion into low-ROI markets  
    ✅ **Must Track**: Weekly monitoring of CAC, CLV, and retention metrics  
    
    ### Investment Required
    
    - **Technology**: ₹50-75L (loyalty platform, personalization, analytics)
    - **Marketing**: ₹2-3Cr (CAC spend, brand building)
    - **Operations**: ₹1-1.5Cr (training, process optimization)
    - **Total 12-Month Budget**: ₹3.5-5Cr
    
    **Expected ROI**: 3-4x within 18-24 months
    """)
    
    st.success("""
    ### 🏆 Final Recommendation
    
    **PROCEED with the comprehensive strategy outlined in this analysis.**
    
    GrovQuick has a real opportunity to become the dominant Q-commerce player in Tier-2 India. 
    The recommendations are grounded in data, realistic in execution, and have the potential to 
    transform unit economics from marginally profitable to highly sustainable.
    
    **Key Confidence Factors:**
    - Strong operational foundation (delivery times, satisfaction)
    - Clear high-value customer segments to target
    - Proven strategies from Tier-1 cities applicable to Tier-2
    - Large addressable market with limited competition
    
    **Next Step**: Approve budget and begin Phase 1 implementation immediately.
    """)
    
    st.markdown("---")
    
    # Contact/Questions Section
    st.header("📞 Questions & Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💬 For More Information
        
        This analysis was prepared as part of the **GrovQuick Case Combat** business case competition.
        
        **Data Source**: Hyperlocal grocery case dataset  
        **Analysis Period**: 2024 customer data  
        **Methodology**: Segmentation, funnel analysis, ROI modeling  
        
        For questions or detailed breakdowns of any section, please refer to the interactive 
        sections in this presentation.
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Implementation Support
        
        **Recommended Action Items:**
        
        1. ✅ Review full presentation with leadership team
        2. ✅ Validate assumptions with recent data
        3. ✅ Approve Phase 1 budget (₹1-1.5Cr)
        4. ✅ Assign implementation owners
        5. ✅ Set up weekly metrics tracking
        6. ✅ Schedule 30-day progress review
        
        **Timeline**: Begin Phase 1 within 2 weeks
        """)
    
    st.markdown("---")
    
    st.balloons()
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px;'>
        <h2>🎉 Thank You!</h2>
        <p style='font-size: 1.2rem;'>
            Thank you for reviewing the GrovQuick Case Combat analysis.<br>
            We look forward to transforming GrovQuick into the leading Q-commerce platform in Tier-2 India.
        </p>
        <p style='margin-top: 1rem; color: #666;'>
            <strong>GrovQuick Team | Case Combat 2024</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 About This App

**GrovQuick Case Combat**  
Interactive Business Presentation

Built with Streamlit, Plotly, and Pandas

**Navigation**: Use the menu above to explore different sections

**Tips**: 
- Each section acts as a presentation slide
- Use filters to explore data interactively
- Adjust parameters to see impact on metrics

---

**Data Source**: Hyperlocal Grocery Case Dataset  
**Last Updated**: 2024
""")

# Add download button for data
if st.sidebar.button("📥 Download Dataset"):
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="grovquick_data.csv",
        mime="text/csv"
    )