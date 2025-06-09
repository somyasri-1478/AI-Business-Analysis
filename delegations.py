"""
API routes for delegation management.
"""
from flask import Blueprint, request, jsonify
from src.services.google_sheets import GoogleSheetsService
import os

delegations_bp = Blueprint('delegations', __name__)

# Initialize Google Sheets service
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID', 'demo_spreadsheet_id')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', None)
sheets_service = GoogleSheetsService(SPREADSHEET_ID, CREDENTIALS_PATH)


@delegations_bp.route('/delegations', methods=['GET'])
def get_delegations():
    """Get all delegations."""
    try:
        delegations = sheets_service.get_delegations()
        return jsonify({
            'success': True,
            'data': delegations,
            'message': 'Delegations retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve delegations'
        }), 500


@delegations_bp.route('/delegations', methods=['POST'])
def create_delegation():
    """Create a new delegation."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['task_delegated', 'person_responsible', 'deadline']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}',
                    'message': 'Invalid delegation data'
                }), 400
        
        # Add delegation to Google Sheets
        success = sheets_service.add_delegation(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Delegation created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create delegation'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create delegation'
        }), 500


@delegations_bp.route('/delegations/by-person/<person>', methods=['GET'])
def get_delegations_by_person(person):
    """Get delegations assigned to a specific person."""
    try:
        all_delegations = sheets_service.get_delegations()
        
        # Filter delegations by person
        person_delegations = [
            delegation for delegation in all_delegations 
            if delegation.get('Person Responsible', '').lower() == person.lower()
        ]
        
        return jsonify({
            'success': True,
            'data': person_delegations,
            'message': f'Delegations for {person} retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f'Failed to retrieve delegations for {person}'
        }), 500


@delegations_bp.route('/delegations/workload-summary', methods=['GET'])
def get_workload_summary():
    """Get workload summary for all team members."""
    try:
        all_delegations = sheets_service.get_delegations()
        team_members = sheets_service.get_team_members()
        
        # Calculate workload for each team member
        workload_summary = {}
        
        for member in team_members:
            name = member.get('Name', '')
            workload_summary[name] = {
                'name': name,
                'department': member.get('Department', ''),
                'role': member.get('Role', ''),
                'total_delegations': 0,
                'pending': 0,
                'in_progress': 0,
                'completed': 0,
                'total_workload_score': 0
            }
        
        # Count delegations by status for each person
        for delegation in all_delegations:
            person = delegation.get('Person Responsible', '')
            status = delegation.get('Status', '')
            workload_score = float(delegation.get('Workload Score', 0))
            
            if person in workload_summary:
                workload_summary[person]['total_delegations'] += 1
                workload_summary[person]['total_workload_score'] += workload_score
                
                if status.lower() == 'pending':
                    workload_summary[person]['pending'] += 1
                elif status.lower() == 'in progress':
                    workload_summary[person]['in_progress'] += 1
                elif status.lower() == 'complete':
                    workload_summary[person]['completed'] += 1
        
        # Convert to list
        summary_list = list(workload_summary.values())
        
        return jsonify({
            'success': True,
            'data': summary_list,
            'message': 'Workload summary retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve workload summary'
        }), 500


@delegations_bp.route('/delegations/overdue', methods=['GET'])
def get_overdue_delegations():
    """Get all overdue delegations."""
    try:
        all_delegations = sheets_service.get_delegations()
        
        # Filter overdue delegations
        from datetime import datetime
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        overdue_delegations = []
        for delegation in all_delegations:
            deadline = delegation.get('Deadline', '')
            status = delegation.get('Status', '')
            
            if deadline and status.lower() not in ['complete'] and deadline < current_date:
                overdue_delegations.append(delegation)
        
        return jsonify({
            'success': True,
            'data': overdue_delegations,
            'message': 'Overdue delegations retrieved successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve overdue delegations'
        }), 500


@delegations_bp.route('/delegations/<delegation_id>/status', methods=['PUT'])
def update_delegation_status(delegation_id):
    """Update delegation status."""
    try:
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing status field',
                'message': 'Invalid request data'
            }), 400
        
        status = data['status']
        valid_statuses = ['Pending', 'In Progress', 'Complete']
        
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'error': f'Invalid status. Must be one of: {valid_statuses}',
                'message': 'Invalid status value'
            }), 400
        
        # In a real implementation, you would update the specific delegation
        # For demo purposes, we'll just return success
        print(f"Mock: Updating delegation {delegation_id} status to {status}")
        
        return jsonify({
            'success': True,
            'message': 'Delegation status updated successfully'
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update delegation status'
        }), 500


@delegations_bp.route('/delegations/<delegation_id>/feedback', methods=['PUT'])
def update_delegation_feedback(delegation_id):
    """Update delegation feedback."""
    try:
        data = request.get_json()
        
        if 'feedback' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing feedback field',
                'message': 'Invalid request data'
            }), 400
        
        feedback = data['feedback']
        
        # In a real implementation, you would update the specific delegation
        # For demo purposes, we'll just return success
        print(f"Mock: Updating delegation {delegation_id} feedback to: {feedback}")
        
        return jsonify({
            'success': True,
            'message': 'Delegation feedback updated successfully'
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update delegation feedback'
        }), 500

