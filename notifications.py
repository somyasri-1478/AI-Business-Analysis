"""
API routes for notification management.
"""
from flask import Blueprint, request, jsonify
from src.services.google_sheets import GoogleSheetsService
from src.services.email_service import EmailNotificationService
from src.services.ai_service import AITaskAnalyzer
import os
from datetime import datetime, timedelta

notifications_bp = Blueprint('notifications', __name__)

# Initialize services
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', 'demo_spreadsheet_id')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', None)
sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_PATH)
email_service = EmailNotificationService()
ai_analyzer = AITaskAnalyzer()


@notifications_bp.route('/notifications/send-task-assignment', methods=['POST'])
def send_task_assignment():
    """Send task assignment notification email."""
    try:
        data = request.get_json()
        
        required_fields = ['assignee_email', 'assignee_name', 'task_data']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'message': 'Invalid request data'
                }), 400
        
        assignee_email = data['assignee_email']
        assignee_name = data['assignee_name']
        task_data = data['task_data']
        
        # Send email notification
        success = email_service.send_task_assignment_email(
            assignee_email, assignee_name, task_data
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Task assignment notification sent successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send task assignment notification'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to send task assignment notification'
        }), 500


@notifications_bp.route('/notifications/send-daily-summary', methods=['POST'])
def send_daily_summary():
    """Send daily task summary to all employees."""
    try:
        # Get all team members
        team_members = sheets_service.get_team_members()
        all_tasks = sheets_service.get_tasks()
        
        results = []
        
        for member in team_members:
            name = member.get('Name', '')
            email = member.get('Email', '')
            
            if not email:
                continue
            
            # Get tasks for this employee
            employee_tasks = [
                task for task in all_tasks 
                if task.get('Assigned To', '').lower() == name.lower() and 
                task.get('Status', '') not in ['Done']
            ]
            
            # Send daily summary
            success = email_service.send_daily_task_summary(
                email, name, employee_tasks
            )
            
            results.append({
                'employee': name,
                'email': email,
                'task_count': len(employee_tasks),
                'sent': success
            })
        
        successful_sends = len([r for r in results if r['sent']])
        
        return jsonify({
            'success': True,
            'data': {
                'total_employees': len(team_members),
                'emails_sent': successful_sends,
                'results': results
            },
            'message': f'Daily summaries sent to {successful_sends} employees'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to send daily summaries'
        }), 500


@notifications_bp.route('/notifications/send-overdue-reminders', methods=['POST'])
def send_overdue_reminders():
    """Send overdue task reminders to employees."""
    try:
        # Get all tasks and team members
        all_tasks = sheets_service.get_tasks()
        team_members = sheets_service.get_team_members()
        
        # Create email lookup
        email_lookup = {member.get('Name', ''): member.get('Email', '') for member in team_members}
        
        # Group overdue tasks by assignee
        overdue_by_assignee = {}
        
        for task in all_tasks:
            assignee = task.get('Assigned To', '')
            due_date = task.get('Due Date', '')
            status = task.get('Status', '')
            
            # Check if task is overdue
            if due_date and status not in ['Done'] and ai_analyzer._is_overdue(due_date):
                if assignee not in overdue_by_assignee:
                    overdue_by_assignee[assignee] = []
                overdue_by_assignee[assignee].append(task)
        
        results = []
        
        for assignee, overdue_tasks in overdue_by_assignee.items():
            email = email_lookup.get(assignee, '')
            
            if not email:
                continue
            
            # Send overdue reminder
            success = email_service.send_overdue_task_reminder(
                email, assignee, overdue_tasks
            )
            
            results.append({
                'employee': assignee,
                'email': email,
                'overdue_count': len(overdue_tasks),
                'sent': success
            })
        
        successful_sends = len([r for r in results if r['sent']])
        
        return jsonify({
            'success': True,
            'data': {
                'employees_with_overdue': len(overdue_by_assignee),
                'reminders_sent': successful_sends,
                'results': results
            },
            'message': f'Overdue reminders sent to {successful_sends} employees'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to send overdue reminders'
        }), 500


@notifications_bp.route('/notifications/send-kpi-alerts', methods=['POST'])
def send_kpi_alerts():
    """Send KPI performance alerts to managers."""
    try:
        data = request.get_json()
        manager_email = data.get('manager_email', 'manager@company.com')
        manager_name = data.get('manager_name', 'Manager')
        
        # Get KPI data and identify alerts
        all_kpis = sheets_service.get_kpis()
        
        # Filter for red status KPIs (underperforming)
        kpi_alerts = []
        for kpi in all_kpis:
            if kpi.get('Status', '') == 'Red':
                alert = {
                    'employee_name': kpi.get('Employee Name', ''),
                    'department': kpi.get('Department', ''),
                    'kpi_name': kpi.get('KPI Name', ''),
                    'target_value': kpi.get('Target Value', ''),
                    'actual_value': kpi.get('Actual Value', ''),
                    'date': kpi.get('Date', ''),
                    'performance_trend': kpi.get('Performance Trend', ''),
                    'severity': 'High' if kpi.get('Performance Trend', '') == 'Declining' else 'Medium'
                }
                kpi_alerts.append(alert)
        
        if not kpi_alerts:
            return jsonify({
                'success': True,
                'message': 'No KPI alerts to send - all metrics are performing well'
            }), 200
        
        # Send KPI alert email
        success = email_service.send_kpi_alert(manager_email, manager_name, kpi_alerts)
        
        if success:
            return jsonify({
                'success': True,
                'data': {
                    'alert_count': len(kpi_alerts),
                    'manager_email': manager_email
                },
                'message': f'KPI alert sent with {len(kpi_alerts)} underperforming metrics'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send KPI alert'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to send KPI alerts'
        }), 500


@notifications_bp.route('/notifications/send-weekly-report', methods=['POST'])
def send_weekly_report():
    """Send weekly performance report."""
    try:
        data = request.get_json()
        recipient_email = data.get('recipient_email', 'manager@company.com')
        recipient_name = data.get('recipient_name', 'Manager')
        
        # Gather weekly report data
        all_tasks = sheets_service.get_tasks()
        all_kpis = sheets_service.get_kpis()
        
        # Calculate task metrics
        completed_tasks = len([t for t in all_tasks if t.get('Status') == 'Done'])
        in_progress_tasks = len([t for t in all_tasks if t.get('Status') == 'In Progress'])
        overdue_tasks = len([t for t in all_tasks if ai_analyzer._is_overdue(t.get('Due Date', ''))])
        
        # Calculate KPI metrics
        green_kpis = len([k for k in all_kpis if k.get('Status') == 'Green'])
        yellow_kpis = len([k for k in all_kpis if k.get('Status') == 'Yellow'])
        red_kpis = len([k for k in all_kpis if k.get('Status') == 'Red'])
        
        report_data = {
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks,
            'green_kpis': green_kpis,
            'yellow_kpis': yellow_kpis,
            'red_kpis': red_kpis
        }
        
        # Send weekly report email
        success = email_service.send_weekly_report(recipient_email, recipient_name, report_data)
        
        if success:
            return jsonify({
                'success': True,
                'data': report_data,
                'message': 'Weekly report sent successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send weekly report'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to send weekly report'
        }), 500


@notifications_bp.route('/notifications/schedule-automated', methods=['POST'])
def schedule_automated_notifications():
    """Schedule automated notifications (placeholder for future implementation)."""
    try:
        data = request.get_json()
        
        notification_types = data.get('notification_types', [])
        schedule_config = data.get('schedule_config', {})
        
        # In a real implementation, this would set up scheduled tasks
        # For now, we'll just return a success response
        
        scheduled_notifications = []
        
        if 'daily_summary' in notification_types:
            scheduled_notifications.append({
                'type': 'daily_summary',
                'schedule': schedule_config.get('daily_time', '09:00'),
                'status': 'scheduled'
            })
        
        if 'overdue_reminders' in notification_types:
            scheduled_notifications.append({
                'type': 'overdue_reminders',
                'schedule': schedule_config.get('reminder_frequency', 'daily'),
                'status': 'scheduled'
            })
        
        if 'weekly_reports' in notification_types:
            scheduled_notifications.append({
                'type': 'weekly_reports',
                'schedule': schedule_config.get('weekly_day', 'Friday'),
                'status': 'scheduled'
            })
        
        return jsonify({
            'success': True,
            'data': {
                'scheduled_notifications': scheduled_notifications,
                'message': 'Automated notifications scheduled successfully'
            },
            'message': f'Scheduled {len(scheduled_notifications)} notification types'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to schedule automated notifications'
        }), 500


@notifications_bp.route('/notifications/test-email', methods=['POST'])
def test_email():
    """Send a test email to verify email configuration."""
    try:
        data = request.get_json()
        
        test_email = data.get('email', 'test@example.com')
        test_name = data.get('name', 'Test User')
        
        # Create test task data
        test_task_data = {
            'task_name': 'Test Task Assignment',
            'task_description': 'This is a test task to verify email functionality',
            'priority': 'Medium',
            'due_date': '2025-06-15',
            'estimated_hours': 4,
            'ai_category': 'Testing'
        }
        
        # Send test email
        success = email_service.send_task_assignment_email(
            test_email, test_name, test_task_data
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Test email sent successfully to {test_email}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send test email'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to send test email'
        }), 500

