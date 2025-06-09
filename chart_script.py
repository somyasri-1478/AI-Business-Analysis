import plotly.graph_objects as go
import plotly.express as px
import json

# Data for the security implementation timeline
data = {
    "phases": [
        {
            "phase": "Phase 1: Basic Authentication",
            "weeks": "Week 1-2",
            "duration": 2,
            "start_week": 1,
            "security_level": "Basic",
            "progress": 85,
            "features": ["Client-side validation", "Local session", "Basic password security"],
            "color": "#3B82F6"
        },
        {
            "phase": "Phase 2: Enhanced Security", 
            "weeks": "Week 3-4",
            "duration": 2,
            "start_week": 3,
            "security_level": "Enhanced",
            "progress": 70,
            "features": ["JWT tokens", "Protected routes", "Input sanitization", "XSS protection"],
            "color": "#F97316"
        },
        {
            "phase": "Phase 3: Advanced Features",
            "weeks": "Week 5-6", 
            "duration": 2,
            "start_week": 5,
            "security_level": "Advanced",
            "progress": 45,
            "features": ["Social login", "2FA", "Password strength", "Session timeout"],
            "color": "#10B981"
        },
        {
            "phase": "Phase 4: Production Hardening",
            "weeks": "Week 7-8",
            "duration": 2,
            "start_week": 7,
            "security_level": "Production", 
            "progress": 25,
            "features": ["HTTPS enforcement", "CSRF protection", "Rate limiting", "Security headers"],
            "color": "#EF4444"
        },
        {
            "phase": "Phase 5: Monitoring & Maintenance",
            "weeks": "Week 9-10",
            "duration": 2,
            "start_week": 9,
            "security_level": "Monitoring",
            "progress": 10,
            "features": ["Audit logging", "Vulnerability scanning", "Performance monitoring", "User analytics"],
            "color": "#8B5CF6"
        }
    ]
}

# Create the timeline chart
fig = go.Figure()

# Add each phase as a horizontal bar
for i, phase in enumerate(data["phases"]):
    # Create comprehensive hover text
    features_list = "<br>• ".join(phase["features"])
    hover_text = f"<b>{phase['phase']}</b><br>{phase['weeks']}<br>Progress: {phase['progress']}%<br><br>Features:<br>• {features_list}"
    
    # Use shorter y-axis labels
    y_label = f"P{i+1}: {phase['security_level']}"
    
    # Add main timeline bar (background)
    fig.add_trace(go.Bar(
        name=phase['security_level'],
        x=[phase["duration"]],
        y=[y_label],
        base=[phase["start_week"] - 1],
        orientation='h',
        marker_color=phase["color"],
        marker_line=dict(color='white', width=1),
        opacity=0.4,
        hovertemplate=hover_text + "<extra></extra>",
        cliponaxis=False
    ))
    
    # Add progress indicator as a filled portion
    progress_width = (phase["duration"] * phase["progress"]) / 100
    fig.add_trace(go.Bar(
        x=[progress_width],
        y=[y_label],
        base=[phase["start_week"] - 1],
        orientation='h',
        marker_color=phase["color"],
        marker_line=dict(color='white', width=1),
        opacity=1.0,
        showlegend=False,
        hovertemplate=hover_text + "<extra></extra>",
        cliponaxis=False
    ))
    
    # Add progress percentage text
    text_x = phase["start_week"] - 1 + (phase["duration"] / 2)
    fig.add_trace(go.Scatter(
        x=[text_x],
        y=[y_label],
        text=[f"{phase['progress']}%"],
        textposition="middle center",
        mode="text",
        showlegend=False,
        hoverinfo="skip",
        textfont=dict(size=12, color="white")
    ))

# Add dependency arrows between phases
for i in range(len(data["phases"]) - 1):
    current_phase = data["phases"][i]
    next_phase = data["phases"][i + 1]
    
    # Arrow from end of current phase to start of next phase
    start_x = current_phase["start_week"] + current_phase["duration"] - 1
    end_x = next_phase["start_week"] - 1
    start_y = i
    end_y = i + 1
    
    fig.add_trace(go.Scatter(
        x=[start_x, end_x],
        y=[f"P{i+1}: {current_phase['security_level']}", f"P{i+2}: {next_phase['security_level']}"],
        mode="lines+markers",
        line=dict(color="gray", width=2),
        marker=dict(symbol="arrow-right", size=8, color="gray"),
        showlegend=False,
        hoverinfo="skip"
    ))

# Update layout
fig.update_layout(
    title="Security Implementation Timeline",
    xaxis_title="Week",
    yaxis_title="Phase",
    barmode='overlay',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update axes
fig.update_xaxes(
    range=[0, 11],
    tickvals=list(range(1, 11)),
    ticktext=[f"W{i}" for i in range(1, 11)]
)

fig.update_yaxes()

# Save the chart
fig.write_image("security_timeline.png")