"""
DEMO SCRIPT: Pistol Shooting Performance Analyzer
This script demonstrates how to use the analyzer programmatically
"""

from shooting_performance_analyzer import (
    ShootingPerformanceAPI,
    ShootingDataManager,
    PerformanceVisualizer,
    PracticeScheduleGenerator
)
from datetime import datetime, timedelta

def demo_mode():
    """Run demo with sample data"""
    print("\n" + "="*70)
    print("DEMO: Pistol Shooting Performance Analyzer".center(70))
    print("="*70)
    
    # Initialize components
    data_manager = ShootingDataManager('demo_shooting_data.json')
    api = ShootingPerformanceAPI()
    
    print("\n[1] Creating sample shooting sessions...\n")
    
    # Sample data
    sample_sessions = [
        {'eights': 3, 'nines': 4, 'tens': 3},
        {'eights': 2, 'nines': 5, 'tens': 3},
        {'eights': 2, 'nines': 4, 'tens': 4},
        {'eights': 1, 'nines': 4, 'tens': 5},
        {'eights': 1, 'nines': 3, 'tens': 6},
    ]
    
    analyses = []
    for idx, session in enumerate(sample_sessions, 1):
        # Create session with date offset for realism
        session_copy = session.copy()
        date_offset = datetime.now() - timedelta(days=(len(sample_sessions)-idx)*3)
        session_copy['date'] = date_offset.strftime('%Y-%m-%d %H:%M:%S')
        
        data_manager.sessions.append(session_copy)
        analysis = api.analyze_session(session_copy)
        analyses.append(analysis)
        
        score = analysis['average_score']
        quality = analysis['session_quality']
        print(f"   Session {idx}: Score {score}/10 - {quality}")
    
    data_manager._save_data()
    
    # Display statistics
    print("\n[2] Session Statistics\n")
    trend = api.get_trend_analysis(analyses)
    print(f"   Total Sessions: {trend['total_sessions']}")
    print(f"   Average Score: {trend['average_score']}/10")
    print(f"   Best Score: {trend['best_score']}/10")
    print(f"   Worst Score: {trend['worst_score']}/10")
    print(f"   Overall Trend: {trend['trend']} →")
    
    # Generate recommendations
    print("\n[3] Personalized Recommendations\n")
    recommendations = api.generate_recommendations(analyses)
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec['focus']}")
        print(f"      Action: {rec['action']}")
        print(f"      Duration: {rec['duration']}\n")
    
    # Generate visualizations
    print("[4] Generating Performance Charts...\n")
    sessions = data_manager.get_all_sessions()
    PerformanceVisualizer.plot_score_trends(sessions, 'demo_score_trends.png')
    PerformanceVisualizer.plot_shot_distribution(sessions, 'demo_shot_distribution.png')
    PerformanceVisualizer.plot_performance_pie(sessions[-1], 'demo_performance_pie.png')
    
    # Generate practice schedule
    print("\n[5] Generating Practice Schedule...\n")
    schedule = PracticeScheduleGenerator.generate_schedule(
        recommendations, 
        days=7, 
        save_path='demo_practice_schedule.txt'
    )
    
    print("\n[6] Sample Practice Schedule (First 500 chars):\n")
    print(schedule[:800])
    print("...\n")
    
    # Detailed report
    print("\n[7] Performance Summary\n")
    print(f"   📊 Sessions Tracked: {trend['total_sessions']}")
    print(f"   📈 Performance Trend: {trend['trend']}")
    print(f"   🎯 Current Average: {trend['average_score']}/10")
    print(f"   🔝 Best Session: {trend['best_score']}/10")
    print(f"   💡 Focus Areas: {len(recommendations)} recommendations")
    
    print("\n" + "="*70)
    print("Demo completed! Files created:".center(70))
    print("="*70)
    print("""
    ✓ demo_shooting_data.json       (Sample data)
    ✓ demo_score_trends.png         (Score trend visualization)
    ✓ demo_shot_distribution.png    (Shot distribution chart)
    ✓ demo_performance_pie.png      (Latest session breakdown)
    ✓ demo_practice_schedule.txt    (Weekly practice plan)
    """)
    
    print("Next Steps:")
    print("  1. Review the generated charts and schedule")
    print("  2. Run 'python shooting_performance_analyzer.py' for interactive mode")
    print("  3. Start tracking your own shooting sessions\n")


if __name__ == "__main__":
    demo_mode()
