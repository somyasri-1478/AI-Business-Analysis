"""
API routes for task management.
"""
from flask import Blueprint, request, jsonify
from src.services.google_sheets import GoogleSheetsService
import os

tasks_bp = Blueprint('tasks', __name__)

# Initialize Google Sheets service
# In production, you would set the actual spreadsheet ID and credentials path
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', 'demo_spreadsheet_id')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', None)
sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_PATH)


@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    try:
        tasks = sheets_service.get_tasks()
        return jsonify({
            'success': True,
            'data': tasks,
            'message': 'Tasks retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve tasks'
        }), 500


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['task_name', 'assigned_to', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'message': 'Invalid task data'
                }), 400
        
        # Add task to Google Sheets
        success = sheets_service.add_task(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Task created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create task'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create task'
        }), 500


@tasks_bp.route('/tasks/<task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    """Update task status."""
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing status field',
                'message': 'Invalid request data'
            }), 400
        
        status = data['status']
        valid_statuses = ['To Do', 'In Progress', 'Done', 'Overdue']
        
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {valid_statuses}',
                'message': 'Invalid status value'
            }), 400
        
        # Update task status in Google Sheets
        success = sheets_service.update_task_status(task_id, status)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Task status updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update task status'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update task status'
        }), 500


@tasks_bp.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    """Get all overdue tasks."""
    try:
        all_tasks = sheets_service.get_tasks()
        
        # Filter overdue tasks (simplified logic for demo)
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        overdue_tasks = []
        for task in all_tasks:
            due_date = task.get('Due Date', '')
            status = task.get('Status', '')
            
            if due_date and status not in ['Done'] and due_date < current_date:
                overdue_tasks.append(task)
        
        return jsonify({
            'success': True,
            'data': overdue_tasks,
            'message': 'Overdue tasks retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve overdue tasks'
        }), 500


@tasks_bp.route('/tasks/by-assignee/<assignee>', methods=['GET'])
def get_tasks_by_assignee(assignee):
    """Get tasks assigned to a specific person."""
    try:
        all_tasks = sheets_service.get_tasks()
        
        # Filter tasks by assignee
        assignee_tasks = [task for task in all_tasks if task.get('Assigned To', '').lower() == assignee.lower()]
        
        return jsonify({
            'success': True,
            'data': assignee_tasks,
            'message': f'Tasks for {assignee} retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to retrieve tasks for {assignee}'
        }), 500


@tasks_bp.route('/tasks/stats', methods=['GET'])
def get_task_stats():
    """Get task statistics."""
    try:
        all_tasks = sheets_service.get_tasks()
        
        # Calculate statistics
        total_tasks = len(all_tasks)
        status_counts = {}
        priority_counts = {}
        
        for task in all_tasks:
            status = task.get('Status', 'Unknown')
            priority = task.get('Priority', 'Unknown')
            
            status_counts[status] = status_counts.get(status, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        stats = {
            'total_tasks': total_tasks,
            'status_breakdown': status_counts,
            'priority_breakdown': priority_counts
        }
        
        return jsonify({
            'success': True,
            'data': stats,
            'message': 'Task statistics retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve task statistics'
        }), 500

