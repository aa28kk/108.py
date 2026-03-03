import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from shooting_performance_analyzer import (
    ShootingDataManager,
    ShootingPerformanceAPI,
    PerformanceVisualizer,
    PracticeScheduleGenerator
)

# Page config
st.set_page_config(page_title="Pistol Shooting Performance Analyzer", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = ShootingDataManager('shooting_sessions.json')
if 'api' not in st.session_state:
    st.session_state.api = ShootingPerformanceAPI(api_key=None)

data_manager = st.session_state.data_manager
api = st.session_state.api

# Header
st.title("🎯 Pistol Shooting Performance Analyzer")
st.markdown("Track your shooting performance, analyze trends, and get personalized practice plans")

# Sidebar Navigation
page = st.sidebar.radio(
    "Select a Section",
    ["🏠 Home", "📝 Add Session", "📊 Statistics & Analytics", "💡 Recommendations", "📅 Practice Schedule", "📈 Visual Reports"]
)

# ============================================================================
# HOME PAGE
# ============================================================================
if page == "🏠 Home":
    st.markdown("## Welcome to Your Shooting Performance Hub")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sessions", len(data_manager.get_all_sessions()))
    
    with col2:
        if len(data_manager.get_all_sessions()) > 0:
            analyses = [api.analyze_session(s) for s in data_manager.get_all_sessions()]
            trend = api.get_trend_analysis(analyses)
            st.metric("Average Score", f"{trend['average_score']}/10")
        else:
            st.metric("Average Score", "N/A")
    
    with col3:
        st.metric("Track Progress", "📌 Add a session to start")
    
    st.markdown("---")
    st.markdown("""
    ### How to Use:
    1. **Add Session** - Record your shooting series (each series is 10 shots)
    2. **Statistics** - View your overall performance and trends
    3. **Recommendations** - Get personalized coaching tips
    4. **Practice Schedule** - Generate a customized weekly training plan
    5. **Visual Reports** - See graphs of your performance trends
    
    ### Shot Categories:
    - **7 or less** - Should-have/cancelled shots
    - **8** - Bad shots
    - **9** - Good shots
    - **10** - Perfect shots
    """)

# ============================================================================
# ADD SESSION PAGE
# ============================================================================
elif page == "📝 Add Session":
    st.header("Record a New Shooting Session")
    st.markdown("A session can contain multiple series. Each series must have exactly 10 shots.")
    
    # Number of series
    num_series = st.number_input("How many series in this session?", min_value=1, max_value=10, value=1)
    
    series_list = []
    for i in range(num_series):
        st.markdown(f"### Series {i+1}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            sevens = st.number_input(f"7 or less (S{i+1})", min_value=0, max_value=10, value=0, key=f"7s_{i}")
        with col2:
            eights = st.number_input(f"8s (S{i+1})", min_value=0, max_value=10, value=0, key=f"8s_{i}")
        with col3:
            nines = st.number_input(f"9s (S{i+1})", min_value=0, max_value=10, value=0, key=f"9s_{i}")
        with col4:
            tens = st.number_input(f"10s (S{i+1})", min_value=0, max_value=10, value=0, key=f"10s_{i}")
        
        total = sevens + eights + nines + tens
        if total == 10:
            st.success(f"✅ Series {i+1} total: {total} shots")
            series_list.append({'seven_or_less': sevens, 'eights': eights, 'nines': nines, 'tens': tens})
        elif total > 0:
            st.warning(f"⚠️ Series {i+1} total: {total}/10 shots")
        else:
            st.info(f"Series {i+1} total: {total}/10 shots")
    
    if st.button("💾 Save Session", use_container_width=True):
        if all(sum([s['seven_or_less'], s['eights'], s['nines'], s['tens']]) == 10 for s in series_list):
            session = data_manager.add_session(series=series_list)
            analysis = api.analyze_session(session)
            
            st.success("✅ Session saved successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Series Count", analysis.get('series_count', 1))
            with col2:
                st.metric("Score (out of 100)", f"{analysis['session_average_100']:.2f}")
            with col3:
                st.metric("Quality", analysis['session_quality'])
            
            if analysis.get('weak_areas'):
                st.markdown("#### Areas for Improvement:")
                for area in analysis['weak_areas']:
                    st.write(f"• {area}")
        else:
            st.error("❌ Each series must total exactly 10 shots!")

# ============================================================================
# STATISTICS PAGE
# ============================================================================
elif page == "📊 Statistics & Analytics":
    st.header("Performance Statistics")
    
    sessions = data_manager.get_all_sessions()
    if not sessions:
        st.warning("No sessions recorded yet. Add a session to see statistics.")
    else:
        analyses = [api.analyze_session(s) for s in sessions]
        trend = api.get_trend_analysis(analyses)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sessions", trend['total_sessions'])
        with col2:
            st.metric("Average Score", f"{trend['average_score']}/10")
        with col3:
            st.metric("Best Score", f"{trend['best_score']}/10")
        with col4:
            st.metric("Worst Score", f"{trend['worst_score']}/10")
        
        st.markdown("---")
        
        # Trend
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### Performance Trend: {trend['trend']}")
        with col2:
            if trend['total_sessions'] >= 2:
                improvement = analyses[-1]['average_score'] - analyses[0]['average_score']
                direction = "📈 Improving" if improvement > 0 else "📉 Declining" if improvement < 0 else "➡️ Stable"
                st.markdown(f"### {direction} ({improvement:+.2f} points)")
        
        st.markdown("---")
        st.markdown("### Recent Sessions")
        
        # Create dataframe
        df_data = []
        for s in sessions[-10:]:
            try:
                from shooting_performance_analyzer import _normalize_session
                norm = _normalize_session(s)
                df_data.append({
                    'Date': s.get('date', ''),
                    'Series': norm['series_count'],
                    '7s<=': norm['total_sevens'],
                    '8s': norm['total_eights'],
                    '9s': norm['total_nines'],
                    '10s': norm['total_tens'],
                    'Total (pts)': f"{norm['session_total_100']:.0f}",
                    'Avg (out of 100)': f"{norm['session_average_100']:.2f}"
                })
            except Exception:
                continue
        
        if df_data:
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)

# ============================================================================
# RECOMMENDATIONS PAGE
# ============================================================================
elif page == "💡 Recommendations":
    st.header("Personalized Coaching Recommendations")
    
    sessions = data_manager.get_all_sessions()
    if not sessions:
        st.warning("No sessions recorded yet. Add sessions to get personalized recommendations.")
    else:
        analyses = [api.analyze_session(s) for s in sessions]
        recommendations = api.generate_recommendations(analyses)
        
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = "🔴" if rec['priority'] == "High" else "🟡"
            
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"{priority_emoji}")
                with col2:
                    st.markdown(f"### {rec['focus']}")
                
                st.markdown(f"**Action:** {rec['action']}")
                st.markdown(f"**Duration:** {rec['duration']}")
                st.markdown("---")

# ============================================================================
# PRACTICE SCHEDULE PAGE
# ============================================================================
elif page == "📅 Practice Schedule":
    st.header("Generate Your Practice Schedule")
    
    sessions = data_manager.get_all_sessions()
    if not sessions:
        st.warning("No sessions recorded yet. Add sessions to generate recommendations and a practice schedule.")
    else:
        analyses = [api.analyze_session(s) for s in sessions]
        recommendations = api.generate_recommendations(analyses)
        
        num_days = st.slider("Schedule duration (days)", min_value=1, max_value=30, value=7)
        
        if st.button("📋 Generate Schedule", use_container_width=True):
            schedule_text = PracticeScheduleGenerator.generate_schedule(
                recommendations,
                days=num_days,
                save_path='practice_schedule.txt'
            )
            
            st.success(f"✅ Practice schedule created for {num_days} days!")
            st.markdown("---")
            st.text_area("Your Practice Schedule", value=schedule_text, height=400, disabled=True)
            
            # Download button
            st.download_button(
                label="📥 Download Schedule",
                data=schedule_text,
                file_name="practice_schedule.txt",
                mime="text/plain"
            )

# ============================================================================
# VISUAL REPORTS PAGE
# ============================================================================
elif page == "📈 Visual Reports":
    st.header("Performance Visualization & Graphs")
    
    sessions = data_manager.get_all_sessions()
    if not sessions:
        st.warning("No sessions recorded yet. Add sessions to see visualizations.")
    else:
        st.markdown("Generating performance charts...")
        
        try:
            # Save charts to temp files
            PerformanceVisualizer.plot_score_trends(sessions, save_path='score_trends.png')
            PerformanceVisualizer.plot_shot_distribution(sessions, save_path='shot_distribution.png')
            PerformanceVisualizer.plot_session_totals(sessions, save_path='session_totals.png')
            PerformanceVisualizer.plot_performance_pie(sessions[-1], save_path='performance_pie.png')
            
            # Display charts in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Score Trends", "Shot Distribution", "Session Totals", "Latest Session"])
            
            with tab1:
                st.image('score_trends.png', use_column_width=True)
            
            with tab2:
                st.image('shot_distribution.png', use_column_width=True)
            
            with tab3:
                st.image('session_totals.png', use_column_width=True)
            
            with tab4:
                st.image('performance_pie.png', use_column_width=True)
            
            st.success("✅ Charts generated successfully!")
            
        except Exception as e:
            st.error(f"Error generating charts: {e}")

# ============================================================================
# SIDEBAR - DATA MANAGEMENT
# ============================================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Data Management")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.data_manager = ShootingDataManager('shooting_sessions.json')
        st.success("Data refreshed!")
    
    if st.button("📥 Download All Sessions", use_container_width=True):
        sessions_json = json.dumps(data_manager.get_all_sessions(), indent=2)
        st.download_button(
            label="JSON",
            data=sessions_json,
            file_name="shooting_sessions.json",
            mime="application/json"
        )
    
    if st.button("🗑️ Clear All Data", use_container_width=True):
        if st.checkbox("Confirm deletion"):
            data_manager.sessions = []
            data_manager._save_data()
            st.success("All data cleared!")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Pistol Shooting Performance Analyzer**
    
    Track your progress, analyze patterns, and improve your shooting skills with data-driven insights.
    
    Features:
    - Multi-series session tracking
    - Performance analytics & trends
    - Personalized coaching tips
    - Auto-generated practice schedules
    - Visual performance reports
    """)
