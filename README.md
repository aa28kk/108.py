# 🎯 Pistol Shooting Performance Analyzer

A comprehensive web-based application for tracking pistol shooting performance, analyzing trends, and generating personalized practice recommendations using Streamlit.

## Features

### 📊 Performance Tracking
- **Multi-Series Sessions**: Record multiple series of 10 shots per session
- **Shot Categories**: Track 7-or-less (should-have/cancelled), 8s (bad), 9s (good), and 10s (perfect) shots
- **Session Aggregation**: Automatic calculation of scores out of 100
- **Score Metrics**: Per-series and session averages, totals, and percentages

### 📈 Analytics & Insights
- **Trend Analysis**: Visualize performance over time
- **Shot Distribution**: See breakdown of shot types across sessions
- **Weak Area Detection**: Automatic identification of areas needing improvement

### 💡 Personalized Coaching
- **Smart Recommendations**: AI-powered coaching tips based on your performance data
- **API Integration**: Optional OpenAI integration for enhanced feedback
- **Practice Plans**: Generate customized weekly practice schedules

### 📊 Visual Reports
- **Score Trend Charts**: Line graphs showing performance progression
- **Shot Distribution**: Stacked bar charts of shot types
- **Session Totals**: Aggregate scores and completion percentages
- **Session Pie Charts**: Breakdown of latest session

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/108.py.git
cd 108.py

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

The app opens at `http://localhost:8501`

## Usage

### 🏠 Home Page
Overview of your sessions and key metrics.

### 📝 Add Session
1. Select number of series (each series = 10 shots)
2. For each series, enter counts:
   - **7 or less**: Should-have/cancelled shots
   - **8**: Bad shots
   - **9**: Good shots
   - **10**: Perfect shots
3. Click "Save Session"

### 📊 Statistics & Analytics
- View aggregated stats across sessions
- Performance trends
- Recent session history
- Quality ratings

### 💡 Recommendations
- High-priority coaching areas
- Medium-priority refinements
- Specific drills and guidance

### 📅 Practice Schedule
- Generate custom schedules (1-30 days)
- Daily session plans with exercises
- Download as text file

### 📈 Visual Reports
- Score trends over time
- Shot type distribution
- Session totals and completion
- Latest session breakdown

## Deployment to Streamlit Cloud

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial Streamlit deployment"
git push origin main
```

2. **Deploy**:
   - Visit [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Select your repo, branch: `main`, file: `app.py`
   - Click "Deploy"

3. **Access**: Your app runs at `https://yourusername-shooting-analyzer.streamlit.app`

## Configuration

### Enable AI Coaching (Optional)
Set your OpenAI API key:

**Local:**
```bash
export SHOOTING_FEEDBACK_API_KEY="sk-..."
streamlit run app.py
```

**Streamlit Cloud:**
- Go to App settings → Secrets
- Add: `SHOOTING_FEEDBACK_API_KEY = "sk-..."`

## Project Structure

```
108.py/
├── app.py                              # Streamlit web interface
├── shooting_performance_analyzer.py    # Core analysis engine
├── feedback_client.py                  # API client
├── requirements.txt                    # Dependencies
├── README.md                           # This file
├── .streamlit/config.toml             # Streamlit config
└── .gitignore                          # Git ignore rules
```

## Score System

| Average | Rating | Status |
|---------|--------|--------|
| 9.5–10.0 | Excellent | 🟢 Perfect |
| 9.0–9.4 | Very Good | 🟢 Great |
| 8.5–8.9 | Good | 🟡 Solid |
| 8.0–8.4 | Fair | 🟡 OK |
| Below 8.0 | Needs Improvement | 🔴 Focus needed |

## Tech Stack

- **Streamlit**: Web framework
- **Pandas**: Data analysis
- **Matplotlib**: Chartsvisualization
- **NumPy**: Numerical computing
- **Requests**: HTTP client

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No sessions recorded" | Click "Add Session" to enter your first data |
| Charts not displaying | Ensure you have at least one session recorded |
| Data not saving | Check file write permissions in app directory |
| API errors | Verify `SHOOTING_FEEDBACK_API_KEY` environment variable |

## License

MIT License – freely available for personal and commercial use.

## Support

- 📧 Issues: GitHub Issues tab
- 💬 Discussions: GitHub Discussions
- 🐛 Bug reports: Include screenshots and steps to reproduce

---

**Happy Shooting! 🎯** Track your progress and improve with consistent, data-driven practice!
