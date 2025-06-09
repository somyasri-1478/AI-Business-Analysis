"""
API routes for KPI management.
"""
from flask import Blueprint, request, jsonify
from src.services.google_sheets import GoogleSheetsService
import os
from datetime import datetime, timedelta

kpis_bp = Blueprint('kpis', __name__)

# Initialize Google Sheets service
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', 'demo_spreadsheet_id')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', None)
sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_PATH)


@kpis_bp.route('/kpis', methods=['GET'])
def get_kpis():
    """Get all KPI entries."""
    try:
        kpis = sheets_service.get_kpis()
        return jsonify({
            'success': True,
            'data': kpis,
            'message': 'KPIs retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve KPIs'
        }), 500


@kpis_bp.route('/kpis', methods=['POST'])
def create_kpi_entry():
    """Create a new KPI entry."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['employee_name', 'department', 'kpi_name', 'target_value', 'actual_value']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'message': 'Invalid KPI data'
                }), 400
        
        # Add KPI entry to Google Sheets
        success = sheets_service.add_kpi_entry(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'KPI entry created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create KPI entry'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create KPI entry'
        }), 500


@kpis_bp.route('/kpis/by-employee/<employee>', methods=['GET'])
def get_kpis_by_employee(employee):
    """Get KPIs for a specific employee."""
    try:
        all_kpis = sheets_service.get_kpis()
        
        # Filter KPIs by employee
        employee_kpis = [
            kpi for kpi in all_kpis 
            if kpi.get('Employee Name', '').lower() == employee.lower()
        ]
        
        return jsonify({
            'success': True,
            'data': employee_kpis,
            'message': f'KPIs for {employee} retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to retrieve KPIs for {employee}'
        }), 500


@kpis_bp.route('/kpis/by-department/<department>', methods=['GET'])
def get_kpis_by_department(department):
    """Get KPIs for a specific department."""
    try:
        all_kpis = sheets_service.get_kpis()
        
        # Filter KPIs by department
        department_kpis = [
            kpi for kpi in all_kpis 
            if kpi.get('Department', '').lower() == department.lower()
        ]
        
        return jsonify({
            'success': True,
            'data': department_kpis,
            'message': f'KPIs for {department} department retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to retrieve KPIs for {department} department'
        }), 500


@kpis_bp.route('/kpis/dashboard', methods=['GET'])
def get_kpi_dashboard():
    """Get KPI dashboard data with summary statistics."""
    try:
        all_kpis = sheets_service.get_kpis()
        
        # Calculate dashboard statistics
        total_kpis = len(all_kpis)
        status_counts = {'Green': 0, 'Yellow': 0, 'Red': 0}
        department_performance = {}
        employee_performance = {}
        
        for kpi in all_kpis:
            status = kpi.get('Status', 'Unknown')
            department = kpi.get('Department', 'Unknown')
            employee = kpi.get('Employee Name', 'Unknown')
            
            # Count status
            if status in status_counts:
                status_counts[status] += 1
            
            # Department performance
            if department not in department_performance:
                department_performance[department] = {'Green': 0, 'Yellow': 0, 'Red': 0, 'total': 0}
            department_performance[department][status] = department_performance[department].get(status, 0) + 1
            department_performance[department]['total'] += 1
            
            # Employee performance
            if employee not in employee_performance:
                employee_performance[employee] = {'Green': 0, 'Yellow': 0, 'Red': 0, 'total': 0}
            employee_performance[employee][status] = employee_performance[employee].get(status, 0) + 1
            employee_performance[employee]['total'] += 1
        
        # Calculate performance percentages
        for dept in department_performance:
            total = department_performance[dept]['total']
            if total > 0:
                department_performance[dept]['green_percentage'] = round((department_performance[dept]['Green'] / total) * 100, 1)
        
        for emp in employee_performance:
            total = employee_performance[emp]['total']
            if total > 0:
                employee_performance[emp]['green_percentage'] = round((employee_performance[emp]['Green'] / total) * 100, 1)
        
        dashboard_data = {
            'total_kpis': total_kpis,
            'status_summary': status_counts,
            'department_performance': department_performance,
            'employee_performance': employee_performance,
            'recent_kpis': all_kpis[-10:] if len(all_kpis) > 10 else all_kpis  # Last 10 entries
        }
        
        return jsonify({
            'success': True,
            'data': dashboard_data,
            'message': 'KPI dashboard data retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve KPI dashboard data'
        }), 500


@kpis_bp.route('/kpis/trends/<employee>', methods=['GET'])
def get_employee_kpi_trends(employee):
    """Get KPI trends for a specific employee."""
    try:
        all_kpis = sheets_service.get_kpis()
        
        # Filter KPIs by employee and sort by date
        employee_kpis = [
            kpi for kpi in all_kpis 
            if kpi.get('Employee Name', '').lower() == employee.lower()
        ]
        
        # Group by KPI name for trend analysis
        kpi_trends = {}
        for kpi in employee_kpis:
            kpi_name = kpi.get('KPI Name', '')
            if kpi_name not in kpi_trends:
                kpi_trends[kpi_name] = []
            
            kpi_trends[kpi_name].append({
                'date': kpi.get('Date', ''),
                'target_value': float(kpi.get('Target Value', 0)),
                'actual_value': float(kpi.get('Actual Value', 0)),
                'status': kpi.get('Status', ''),
                'performance_trend': kpi.get('Performance Trend', '')
            })
        
        # Sort each KPI trend by date
        for kpi_name in kpi_trends:
            kpi_trends[kpi_name].sort(key=lambda x: x['date'])
        
        return jsonify({
            'success': True,
            'data': {
                'employee': employee,
                'kpi_trends': kpi_trends
            },
            'message': f'KPI trends for {employee} retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to retrieve KPI trends for {employee}'
        }), 500


@kpis_bp.route('/kpis/alerts', methods=['GET'])
def get_kpi_alerts():
    """Get KPI alerts for underperforming metrics."""
    try:
        all_kpis = sheets_service.get_kpis()
        
        # Filter for Red status KPIs (underperforming)
        alerts = []
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
                alerts.append(alert)
        
        # Sort by severity and date
        alerts.sort(key=lambda x: (x['severity'] == 'High', x['date']), reverse=True)
        
        return jsonify({
            'success': True,
            'data': alerts,
            'message': 'KPI alerts retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve KPI alerts'
        }), 500


@kpis_bp.route('/kpis/monthly-summary', methods=['GET'])
def get_monthly_kpi_summary():
    """Get monthly KPI summary."""
    try:
        all_kpis = sheets_service.get_kpis()
        
        # Get current month data
        current_month = datetime.now().strftime('%Y-%m')
        monthly_kpis = [
            kpi for kpi in all_kpis 
            if kpi.get('Date', '').startswith(current_month)
        ]
        
        # Calculate monthly statistics
        monthly_stats = {
            'month': current_month,
            'total_entries': len(monthly_kpis),
            'status_breakdown': {'Green': 0, 'Yellow': 0, 'Red': 0},
            'department_summary': {},
            'top_performers': [],
            'improvement_needed': []
        }
        
        department_scores = {}
        employee_scores = {}
        
        for kpi in monthly_kpis:
            status = kpi.get('Status', '')
            department = kpi.get('Department', '')
            employee = kpi.get('Employee Name', '')
            
            # Status breakdown
            if status in monthly_stats['status_breakdown']:
                monthly_stats['status_breakdown'][status] += 1
            
            # Department tracking
            if department not in department_scores:
                department_scores[department] = {'green': 0, 'total': 0}
            department_scores[department]['total'] += 1
            if status == 'Green':
                department_scores[department]['green'] += 1
            
            # Employee tracking
            if employee not in employee_scores:
                employee_scores[employee] = {'green': 0, 'total': 0, 'department': department}
            employee_scores[employee]['total'] += 1
            if status == 'Green':
                employee_scores[employee]['green'] += 1
        
        # Calculate department performance percentages
        for dept, scores in department_scores.items():
            percentage = (scores['green'] / scores['total']) * 100 if scores['total'] > 0 else 0
            monthly_stats['department_summary'][dept] = {
                'green_percentage': round(percentage, 1),
                'total_kpis': scores['total']
            }
        
        # Identify top performers and those needing improvement
        for emp, scores in employee_scores.items():
            percentage = (scores['green'] / scores['total']) * 100 if scores['total'] > 0 else 0
            emp_data = {
                'name': emp,
                'department': scores['department'],
                'green_percentage': round(percentage, 1),
                'total_kpis': scores['total']
            }
            
            if percentage >= 80:
                monthly_stats['top_performers'].append(emp_data)
            elif percentage < 50:
                monthly_stats['improvement_needed'].append(emp_data)
        
        # Sort lists
        monthly_stats['top_performers'].sort(key=lambda x: x['green_percentage'], reverse=True)
        monthly_stats['improvement_needed'].sort(key=lambda x: x['green_percentage'])
        
        return jsonify({
            'success': True,
            'data': monthly_stats,
            'message': 'Monthly KPI summary retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve monthly KPI summary'
        }), 500

