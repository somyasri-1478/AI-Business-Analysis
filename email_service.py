"""
Email notification service for task assignments and reminders.
"""
import smtplib
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json


class EmailNotificationService:
    """Service for sending email notifications."""
    
    def __init__(self):
        """Initialize email service with configuration."""
        # Email configuration (in production, use environment variables)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', 'your-email@gmail.com')
        self.email_password = os.getenv('EMAIL_PASSWORD', 'your-app-password')
        self.from_name = os.getenv('FROM_NAME', 'Business Systems AI')
        
        # For demo purposes, we'll simulate email sending
        self.demo_mode = True
        
    def send_task_assignment_email(self, assignee_email: str, assignee_name: str, 
                                 task_data: Dict[str, Any]) -> bool:
        """
        Send task assignment email to team member.
        
        Args:
            assignee_email: Email address of the assignee
            assignee_name: Name of the assignee
            task_data: Task information
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            subject = f"New Task Assignment: {task_data.get('task_name', 'Unnamed Task')}"
            
            # Create email content
            html_content = self._create_task_assignment_html(assignee_name, task_data)
            text_content = self._create_task_assignment_text(assignee_name, task_data)
            
            # Send email
            return self._send_email(
                to_email=assignee_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            print(f"Error sending task assignment email: {e}")
            return False
    
    def send_daily_task_summary(self, employee_email: str, employee_name: str, 
                              daily_tasks: List[Dict[str, Any]]) -> bool:
        """
        Send daily task summary email to employee.
        
        Args:
            employee_email: Email address of the employee
            employee_name: Name of the employee
            daily_tasks: List of tasks for the day
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            today = datetime.now().strftime('%B %d, %Y')
            subject = f"Daily Task Summary - {today}"
            
            # Create email content
            html_content = self._create_daily_summary_html(employee_name, daily_tasks, today)
            text_content = self._create_daily_summary_text(employee_name, daily_tasks, today)
            
            # Send email
            return self._send_email(
                to_email=employee_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            print(f"Error sending daily task summary: {e}")
            return False
    
    def send_overdue_task_reminder(self, assignee_email: str, assignee_name: str, 
                                 overdue_tasks: List[Dict[str, Any]]) -> bool:
        """
        Send overdue task reminder email.
        
        Args:
            assignee_email: Email address of the assignee
            assignee_name: Name of the assignee
            overdue_tasks: List of overdue tasks
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            subject = f"Overdue Task Reminder - {len(overdue_tasks)} task(s) need attention"
            
            # Create email content
            html_content = self._create_overdue_reminder_html(assignee_name, overdue_tasks)
            text_content = self._create_overdue_reminder_text(assignee_name, overdue_tasks)
            
            # Send email
            return self._send_email(
                to_email=assignee_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            print(f"Error sending overdue task reminder: {e}")
            return False
    
    def send_kpi_alert(self, manager_email: str, manager_name: str, 
                      kpi_alerts: List[Dict[str, Any]]) -> bool:
        """
        Send KPI performance alert email to manager.
        
        Args:
            manager_email: Email address of the manager
            manager_name: Name of the manager
            kpi_alerts: List of KPI alerts
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            subject = f"KPI Performance Alert - {len(kpi_alerts)} metric(s) need attention"
            
            # Create email content
            html_content = self._create_kpi_alert_html(manager_name, kpi_alerts)
            text_content = self._create_kpi_alert_text(manager_name, kpi_alerts)
            
            # Send email
            return self._send_email(
                to_email=manager_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            print(f"Error sending KPI alert: {e}")
            return False
    
    def send_weekly_report(self, recipient_email: str, recipient_name: str, 
                          report_data: Dict[str, Any]) -> bool:
        """
        Send weekly performance report email.
        
        Args:
            recipient_email: Email address of the recipient
            recipient_name: Name of the recipient
            report_data: Weekly report data
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            week_ending = datetime.now().strftime('%B %d, %Y')
            subject = f"Weekly Performance Report - Week Ending {week_ending}"
            
            # Create email content
            html_content = self._create_weekly_report_html(recipient_name, report_data, week_ending)
            text_content = self._create_weekly_report_text(recipient_name, report_data, week_ending)
            
            # Send email
            return self._send_email(
                to_email=recipient_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
        except Exception as e:
            print(f"Error sending weekly report: {e}")
            return False
    
    def _send_email(self, to_email: str, subject: str, 
                   html_content: str, text_content: str) -> bool:
        """
        Send email using SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if self.demo_mode:
            # In demo mode, just log the email instead of sending
            print(f"\n=== EMAIL NOTIFICATION (DEMO MODE) ===")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content Preview: {text_content[:200]}...")
            print("=== END EMAIL ===\n")
            return True
        
        try:
            # For production, you would implement actual SMTP email sending here
            # For now, we'll just simulate successful sending
            print(f"Email would be sent to {to_email} with subject: {subject}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _create_task_assignment_html(self, assignee_name: str, task_data: Dict[str, Any]) -> str:
        """Create HTML content for task assignment email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .task-details {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }}
                .priority-high {{ border-left-color: #f44336; }}
                .priority-medium {{ border-left-color: #ff9800; }}
                .priority-low {{ border-left-color: #2196F3; }}
                .footer {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Task Assignment</h1>
                </div>
                <div class="content">
                    <p>Hello {assignee_name},</p>
                    <p>You have been assigned a new task. Please review the details below:</p>
                    
                    <div class="task-details priority-{task_data.get('priority', 'medium').lower()}">
                        <h3>{task_data.get('task_name', 'Unnamed Task')}</h3>
                        <p><strong>Description:</strong> {task_data.get('task_description', 'No description provided')}</p>
                        <p><strong>Priority:</strong> {task_data.get('priority', 'Medium')}</p>
                        <p><strong>Due Date:</strong> {task_data.get('due_date', 'Not specified')}</p>
                        <p><strong>Estimated Hours:</strong> {task_data.get('estimated_hours', 'Not specified')}</p>
                        <p><strong>Category:</strong> {task_data.get('ai_category', 'General')}</p>
                    </div>
                    
                    <p>Please log into the business systems dashboard to view more details and update your progress.</p>
                    
                    <p>If you have any questions about this task, please contact your project manager.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from the Business Systems AI.</p>
                    <p>Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_task_assignment_text(self, assignee_name: str, task_data: Dict[str, Any]) -> str:
        """Create plain text content for task assignment email."""
        return f"""
        NEW TASK ASSIGNMENT
        
        Hello {assignee_name},
        
        You have been assigned a new task. Please review the details below:
        
        Task Name: {task_data.get('task_name', 'Unnamed Task')}
        Description: {task_data.get('task_description', 'No description provided')}
        Priority: {task_data.get('priority', 'Medium')}
        Due Date: {task_data.get('due_date', 'Not specified')}
        Estimated Hours: {task_data.get('estimated_hours', 'Not specified')}
        Category: {task_data.get('ai_category', 'General')}
        
        Please log into the business systems dashboard to view more details and update your progress.
        
        If you have any questions about this task, please contact your project manager.
        
        ---
        This is an automated message from the Business Systems AI.
        Please do not reply to this email.
        """
    
    def _create_daily_summary_html(self, employee_name: str, daily_tasks: List[Dict[str, Any]], date: str) -> str:
        """Create HTML content for daily task summary email."""
        tasks_html = ""
        for task in daily_tasks:
            priority_class = f"priority-{task.get('Priority', 'medium').lower()}"
            tasks_html += f"""
            <div class="task-item {priority_class}">
                <h4>{task.get('Task Name', 'Unnamed Task')}</h4>
                <p><strong>Priority:</strong> {task.get('Priority', 'Medium')}</p>
                <p><strong>Due Date:</strong> {task.get('Due Date', 'Not specified')}</p>
                <p><strong>Status:</strong> {task.get('Status', 'To Do')}</p>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #2196F3; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .task-item {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #2196F3; }}
                .priority-high {{ border-left-color: #f44336; }}
                .priority-medium {{ border-left-color: #ff9800; }}
                .priority-low {{ border-left-color: #4CAF50; }}
                .footer {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Daily Task Summary</h1>
                    <p>{date}</p>
                </div>
                <div class="content">
                    <p>Hello {employee_name},</p>
                    <p>Here are your tasks for today ({len(daily_tasks)} total):</p>
                    
                    {tasks_html}
                    
                    <p>Have a productive day!</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from the Business Systems AI.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_daily_summary_text(self, employee_name: str, daily_tasks: List[Dict[str, Any]], date: str) -> str:
        """Create plain text content for daily task summary email."""
        tasks_text = ""
        for i, task in enumerate(daily_tasks, 1):
            tasks_text += f"""
        {i}. {task.get('Task Name', 'Unnamed Task')}
           Priority: {task.get('Priority', 'Medium')}
           Due Date: {task.get('Due Date', 'Not specified')}
           Status: {task.get('Status', 'To Do')}
        """
        
        return f"""
        DAILY TASK SUMMARY - {date}
        
        Hello {employee_name},
        
        Here are your tasks for today ({len(daily_tasks)} total):
        {tasks_text}
        
        Have a productive day!
        
        ---
        This is an automated message from the Business Systems AI.
        """
    
    def _create_overdue_reminder_html(self, assignee_name: str, overdue_tasks: List[Dict[str, Any]]) -> str:
        """Create HTML content for overdue task reminder email."""
        tasks_html = ""
        for task in overdue_tasks:
            tasks_html += f"""
            <div class="task-item overdue">
                <h4>{task.get('Task Name', 'Unnamed Task')}</h4>
                <p><strong>Due Date:</strong> {task.get('Due Date', 'Not specified')}</p>
                <p><strong>Priority:</strong> {task.get('Priority', 'Medium')}</p>
                <p><strong>Status:</strong> {task.get('Status', 'To Do')}</p>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #f44336; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .task-item {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #f44336; }}
                .footer {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Overdue Task Reminder</h1>
                </div>
                <div class="content">
                    <p>Hello {assignee_name},</p>
                    <p>You have {len(overdue_tasks)} overdue task(s) that need immediate attention:</p>
                    
                    {tasks_html}
                    
                    <p>Please update these tasks as soon as possible and contact your manager if you need assistance.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from the Business Systems AI.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_overdue_reminder_text(self, assignee_name: str, overdue_tasks: List[Dict[str, Any]]) -> str:
        """Create plain text content for overdue task reminder email."""
        tasks_text = ""
        for i, task in enumerate(overdue_tasks, 1):
            tasks_text += f"""
        {i}. {task.get('Task Name', 'Unnamed Task')}
           Due Date: {task.get('Due Date', 'Not specified')}
           Priority: {task.get('Priority', 'Medium')}
           Status: {task.get('Status', 'To Do')}
        """
        
        return f"""
        ⚠️ OVERDUE TASK REMINDER
        
        Hello {assignee_name},
        
        You have {len(overdue_tasks)} overdue task(s) that need immediate attention:
        {tasks_text}
        
        Please update these tasks as soon as possible and contact your manager if you need assistance.
        
        ---
        This is an automated message from the Business Systems AI.
        """
    
    def _create_kpi_alert_html(self, manager_name: str, kpi_alerts: List[Dict[str, Any]]) -> str:
        """Create HTML content for KPI alert email."""
        alerts_html = ""
        for alert in kpi_alerts:
            alerts_html += f"""
            <div class="alert-item">
                <h4>{alert.get('employee_name', 'Unknown')} - {alert.get('kpi_name', 'Unknown KPI')}</h4>
                <p><strong>Department:</strong> {alert.get('department', 'Unknown')}</p>
                <p><strong>Target:</strong> {alert.get('target_value', 'N/A')}</p>
                <p><strong>Actual:</strong> {alert.get('actual_value', 'N/A')}</p>
                <p><strong>Trend:</strong> {alert.get('performance_trend', 'Unknown')}</p>
                <p><strong>Severity:</strong> {alert.get('severity', 'Medium')}</p>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ff9800; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .alert-item {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #ff9800; }}
                .footer {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 KPI Performance Alert</h1>
                </div>
                <div class="content">
                    <p>Hello {manager_name},</p>
                    <p>The following KPI metrics require your attention:</p>
                    
                    {alerts_html}
                    
                    <p>Please review these metrics and take appropriate action to improve performance.</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from the Business Systems AI.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_kpi_alert_text(self, manager_name: str, kpi_alerts: List[Dict[str, Any]]) -> str:
        """Create plain text content for KPI alert email."""
        alerts_text = ""
        for i, alert in enumerate(kpi_alerts, 1):
            alerts_text += f"""
        {i}. {alert.get('employee_name', 'Unknown')} - {alert.get('kpi_name', 'Unknown KPI')}
           Department: {alert.get('department', 'Unknown')}
           Target: {alert.get('target_value', 'N/A')}
           Actual: {alert.get('actual_value', 'N/A')}
           Trend: {alert.get('performance_trend', 'Unknown')}
           Severity: {alert.get('severity', 'Medium')}
        """
        
        return f"""
        📊 KPI PERFORMANCE ALERT
        
        Hello {manager_name},
        
        The following KPI metrics require your attention:
        {alerts_text}
        
        Please review these metrics and take appropriate action to improve performance.
        
        ---
        This is an automated message from the Business Systems AI.
        """
    
    def _create_weekly_report_html(self, recipient_name: str, report_data: Dict[str, Any], week_ending: str) -> str:
        """Create HTML content for weekly report email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #673AB7; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9f9f9; }}
                .metric {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #673AB7; }}
                .footer {{ text-align: center; padding: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📈 Weekly Performance Report</h1>
                    <p>Week Ending {week_ending}</p>
                </div>
                <div class="content">
                    <p>Hello {recipient_name},</p>
                    <p>Here's your weekly performance summary:</p>
                    
                    <div class="metric">
                        <h4>Task Completion</h4>
                        <p>Completed: {report_data.get('completed_tasks', 0)} tasks</p>
                        <p>In Progress: {report_data.get('in_progress_tasks', 0)} tasks</p>
                        <p>Overdue: {report_data.get('overdue_tasks', 0)} tasks</p>
                    </div>
                    
                    <div class="metric">
                        <h4>KPI Performance</h4>
                        <p>Green Status: {report_data.get('green_kpis', 0)} KPIs</p>
                        <p>Yellow Status: {report_data.get('yellow_kpis', 0)} KPIs</p>
                        <p>Red Status: {report_data.get('red_kpis', 0)} KPIs</p>
                    </div>
                    
                    <p>Keep up the great work!</p>
                </div>
                <div class="footer">
                    <p>This is an automated message from the Business Systems AI.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_weekly_report_text(self, recipient_name: str, report_data: Dict[str, Any], week_ending: str) -> str:
        """Create plain text content for weekly report email."""
        return f"""
        📈 WEEKLY PERFORMANCE REPORT
        Week Ending {week_ending}
        
        Hello {recipient_name},
        
        Here's your weekly performance summary:
        
        TASK COMPLETION:
        - Completed: {report_data.get('completed_tasks', 0)} tasks
        - In Progress: {report_data.get('in_progress_tasks', 0)} tasks
        - Overdue: {report_data.get('overdue_tasks', 0)} tasks
        
        KPI PERFORMANCE:
        - Green Status: {report_data.get('green_kpis', 0)} KPIs
        - Yellow Status: {report_data.get('yellow_kpis', 0)} KPIs
        - Red Status: {report_data.get('red_kpis', 0)} KPIs
        
        Keep up the great work!
        
        ---
        This is an automated message from the Business Systems AI.
        """

