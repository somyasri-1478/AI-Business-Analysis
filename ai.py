"""
API routes for AI-powered features.
"""
from flask import Blueprint, request, jsonify
from src.services.google_sheets import GoogleSheetsService
from src.services.ai_service import AITaskAnalyzer
import os

ai_bp = Blueprint('ai', __name__)

# Initialize services
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', 'demo_spreadsheet_id')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', None)
sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_PATH)
ai_analyzer = AITaskAnalyzer()


@ai_bp.route('/ai/categorize-task', methods=['POST'])
def categorize_task():
    """Categorize a task using AI analysis."""
    try:
        data = request.get_json()
        
        if 'task_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing task_name field',
                'message': 'Invalid request data'
            }), 400
        
        task_name = data['task_name']
        task_description = data.get('task_description', '')
        
        # Use AI to categorize the task
        result = ai_analyzer.categorize_task(task_name, task_description)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Task categorized successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to categorize task'
        }), 500


@ai_bp.route('/ai/suggest-priority', methods=['POST'])
def suggest_priority():
    """Suggest task priority using AI analysis."""
    try:
        data = request.get_json()
        
        if 'task_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing task_name field',
                'message': 'Invalid request data'
            }), 400
        
        task_name = data['task_name']
        task_description = data.get('task_description', '')
        due_date = data.get('due_date', '')
        
        # Use AI to suggest priority
        result = ai_analyzer.suggest_priority(task_name, task_description, due_date)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Priority suggested successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to suggest priority'
        }), 500


@ai_bp.route('/ai/suggest-deadline', methods=['POST'])
def suggest_deadline():
    """Suggest task deadline using AI analysis."""
    try:
        data = request.get_json()
        
        if 'task_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing task_name field',
                'message': 'Invalid request data'
            }), 400
        
        task_name = data['task_name']
        task_description = data.get('task_description', '')
        priority = data.get('priority', 'Medium')
        estimated_hours = data.get('estimated_hours', 8)
        
        # Use AI to suggest deadline
        result = ai_analyzer.suggest_deadline(task_name, task_description, priority, estimated_hours)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Deadline suggested successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to suggest deadline'
        }), 500


@ai_bp.route('/ai/analyze-workload', methods=['GET'])
def analyze_workload():
    """Analyze team workload distribution using AI."""
    try:
        # Get team members and current tasks
        team_members = sheets_service.get_team_members()
        current_tasks = sheets_service.get_tasks()
        
        # Use AI to analyze workload
        result = ai_analyzer.analyze_workload_distribution(team_members, current_tasks)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Workload analysis completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to analyze workload'
        }), 500


@ai_bp.route('/ai/predict-performance', methods=['GET'])
def predict_performance():
    """Predict performance trends using AI analysis."""
    try:
        # Get KPI history
        kpi_history = sheets_service.get_kpis()
        
        # Use AI to predict performance trends
        result = ai_analyzer.predict_performance_trend(kpi_history)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Performance prediction completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to predict performance'
        }), 500


@ai_bp.route('/ai/break-down-task', methods=['POST'])
def break_down_task():
    """Break down a large task into subtasks using AI."""
    try:
        data = request.get_json()
        
        required_fields = ['task_name', 'task_description', 'estimated_hours']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'message': 'Invalid request data'
                }), 400
        
        task_name = data['task_name']
        task_description = data['task_description']
        estimated_hours = data['estimated_hours']
        team_size = data.get('team_size', 1)
        
        # Use AI to break down the task
        result = ai_analyzer.break_down_task(task_name, task_description, estimated_hours, team_size)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Task breakdown completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to break down task'
        }), 500


@ai_bp.route('/ai/generate-insights', methods=['GET'])
def generate_insights():
    """Generate AI-powered insights from dashboard data."""
    try:
        # Gather dashboard data
        tasks = sheets_service.get_tasks()
        kpis = sheets_service.get_kpis()
        delegations = sheets_service.get_delegations()
        
        dashboard_data = {
            'tasks': tasks,
            'kpis': kpis,
            'delegations': delegations
        }
        
        # Use AI to generate insights
        result = ai_analyzer.generate_insights(dashboard_data)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Insights generated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate insights'
        }), 500


@ai_bp.route('/ai/smart-task-assignment', methods=['POST'])
def smart_task_assignment():
    """Suggest optimal task assignment using AI analysis."""
    try:
        data = request.get_json()
        
        if 'task_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing task_name field',
                'message': 'Invalid request data'
            }), 400
        
        task_name = data['task_name']
        task_description = data.get('task_description', '')
        required_skills = data.get('required_skills', '')
        priority = data.get('priority', 'Medium')
        
        # Get team members and analyze workload
        team_members = sheets_service.get_team_members()
        current_tasks = sheets_service.get_tasks()
        workload_analysis = ai_analyzer.analyze_workload_distribution(team_members, current_tasks)
        
        # Categorize the task to understand skill requirements
        task_category = ai_analyzer.categorize_task(task_name, task_description)
        
        # Find best assignee based on workload and skills
        best_assignee = None
        best_score = -1
        assignment_reasoning = []
        
        for member_name, workload_info in workload_analysis['workload_analysis'].items():
            # Calculate assignment score
            capacity_score = workload_info['capacity_available'] / 100  # 0-1 scale
            
            # Simple skill matching (in a real system, this would be more sophisticated)
            skill_score = 0.5  # Default skill match
            member_role = workload_info.get('role', '').lower()
            task_cat = task_category['category'].lower()
            
            if 'developer' in member_role and 'development' in task_cat:
                skill_score = 0.9
            elif 'manager' in member_role and 'project' in task_cat:
                skill_score = 0.9
            elif 'analyst' in member_role and 'analysis' in task_cat:
                skill_score = 0.9
            elif 'marketing' in member_role and 'marketing' in task_cat:
                skill_score = 0.9
            
            # Priority adjustment (high priority tasks go to less loaded members)
            priority_adjustment = 1.0
            if priority == 'High' and workload_info['workload_score'] > 70:
                priority_adjustment = 0.7
            
            # Calculate final score
            final_score = (capacity_score * 0.4 + skill_score * 0.6) * priority_adjustment
            
            if final_score > best_score:
                best_score = final_score
                best_assignee = member_name
                assignment_reasoning = [
                    f"Capacity available: {workload_info['capacity_available']}%",
                    f"Skill match: {skill_score * 100:.0f}%",
                    f"Current workload: {workload_info['workload_status']}",
                    f"Final score: {final_score:.2f}"
                ]
        
        result = {
            'recommended_assignee': best_assignee,
            'confidence_score': round(best_score, 2),
            'assignment_reasoning': assignment_reasoning,
            'task_analysis': task_category,
            'alternative_assignees': []
        }
        
        # Find alternative assignees
        sorted_members = sorted(
            workload_analysis['workload_analysis'].items(),
            key=lambda x: x[1]['capacity_available'],
            reverse=True
        )
        
        for member_name, workload_info in sorted_members[:3]:
            if member_name != best_assignee:
                result['alternative_assignees'].append({
                    'name': member_name,
                    'capacity_available': workload_info['capacity_available'],
                    'workload_status': workload_info['workload_status'],
                    'current_tasks': workload_info['total_tasks']
                })
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Smart task assignment completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to suggest task assignment'
        }), 500


@ai_bp.route('/ai/optimize-schedule', methods=['POST'])
def optimize_schedule():
    """Optimize task schedule using AI analysis."""
    try:
        data = request.get_json()
        
        # Get current tasks
        current_tasks = sheets_service.get_tasks()
        
        # Analyze task dependencies and priorities
        optimization_result = {
            'optimized_schedule': [],
            'recommendations': [],
            'potential_conflicts': [],
            'efficiency_improvements': []
        }
        
        # Sort tasks by priority and deadline
        high_priority_tasks = [t for t in current_tasks if t.get('Priority') == 'High']
        medium_priority_tasks = [t for t in current_tasks if t.get('Priority') == 'Medium']
        low_priority_tasks = [t for t in current_tasks if t.get('Priority') == 'Low']
        
        # Generate recommendations
        if len(high_priority_tasks) > 5:
            optimization_result['recommendations'].append(
                f"Consider breaking down {len(high_priority_tasks)} high-priority tasks into smaller chunks"
            )
        
        if len([t for t in current_tasks if ai_analyzer._is_overdue(t.get('Due Date', ''))]) > 0:
            optimization_result['recommendations'].append(
                "Reschedule overdue tasks and adjust future deadlines accordingly"
            )
        
        optimization_result['recommendations'].extend([
            "Group similar tasks together for better focus",
            "Schedule high-priority tasks during peak productivity hours",
            "Leave buffer time between complex tasks"
        ])
        
        return jsonify({
            'success': True,
            'data': optimization_result,
            'message': 'Schedule optimization completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to optimize schedule'
        }), 500

