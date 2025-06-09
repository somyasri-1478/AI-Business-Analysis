"""
Google Sheets API service for business systems integration.
"""
import os
import json
from typing import List, Dict, Any, Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from datetime import datetime, timedelta


class GoogleSheetsService:
    """Service class for Google Sheets API operations."""
    
    def __init__(self, spreadsheet_id: str, credentials_path: Optional[str] = None):
        """
        Initialize Google Sheets service.
        
        Args:
            spreadsheet_id: The ID of the Google Spreadsheet
            credentials_path: Path to service account credentials JSON file
        """
        self.spreadsheet_id = spreadsheet_id
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        
        # For demo purposes, we'll use a mock service
        # In production, you would use actual Google Sheets API credentials
        self.service = None
        self._init_service(credentials_path)
    
    def _init_service(self, credentials_path: Optional[str]):
        """Initialize Google Sheets API service."""
        try:
            if credentials_path and os.path.exists(credentials_path):
                credentials = Credentials.from_service_account_file(
                    credentials_path, scopes=self.scopes
                )
                self.service = build('sheets', 'v4', credentials=credentials)
            else:
                # Mock service for demo - in production, you'd need actual credentials
                print("Warning: Using mock Google Sheets service. Set up actual credentials for production.")
                self.service = None
        except Exception as e:
            print(f"Error initializing Google Sheets service: {e}")
            self.service = None
    
    def read_sheet_data(self, sheet_name: str, range_name: str = None) -> List[List[str]]:
        """
        Read data from a Google Sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            range_name: Optional range specification (e.g., 'A1:E10')
            
        Returns:
            List of rows, where each row is a list of cell values
        """
        if not self.service:
            # Return mock data for demo
            return self._get_mock_data(sheet_name)
        
        try:
            range_spec = f"{sheet_name}!{range_name}" if range_name else sheet_name
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_spec
            ).execute()
            
            values = result.get('values', [])
            return values
        except HttpError as e:
            print(f"Error reading sheet data: {e}")
            return []
    
    def write_sheet_data(self, sheet_name: str, data: List[List[Any]], range_name: str = None) -> bool:
        """
        Write data to a Google Sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            data: Data to write (list of rows)
            range_name: Optional range specification
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            print(f"Mock: Writing data to {sheet_name}: {len(data)} rows")
            return True
        
        try:
            range_spec = f"{sheet_name}!{range_name}" if range_name else sheet_name
            body = {'values': data}
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_spec,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return True
        except HttpError as e:
            print(f"Error writing sheet data: {e}")
            return False
    
    def append_sheet_data(self, sheet_name: str, data: List[List[Any]]) -> bool:
        """
        Append data to a Google Sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            data: Data to append (list of rows)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            print(f"Mock: Appending data to {sheet_name}: {len(data)} rows")
            return True
        
        try:
            body = {'values': data}
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            return True
        except HttpError as e:
            print(f"Error appending sheet data: {e}")
            return False
    
    def _get_mock_data(self, sheet_name: str) -> List[List[str]]:
        """Return mock data for demo purposes."""
        if sheet_name == "Master_Tasks":
            return [
                ["Task ID", "Task Name", "Assigned To", "Due Date", "Priority", "Status", "Frequency", "Completion Timestamp", "Suggested Deadline", "AI Category"],
                ["1", "Complete project proposal", "John Doe", "2025-06-15", "High", "In Progress", "One-time", "", "2025-06-14", "Project Management"],
                ["2", "Review quarterly reports", "Jane Smith", "2025-06-20", "Medium", "To Do", "Monthly", "", "2025-06-18", "Analysis"],
                ["3", "Update website content", "Bob Johnson", "2025-06-12", "Low", "Done", "Weekly", "2025-06-10 14:30:00", "2025-06-12", "Content Management"]
            ]
        elif sheet_name == "Delegation_Tracker":
            return [
                ["Delegation ID", "Task Delegated", "Person Responsible", "Deadline", "Status", "Feedback/Comments", "Workload Score"],
                ["1", "Complete project proposal", "John Doe", "2025-06-15", "In Progress", "Making good progress", "7"],
                ["2", "Review quarterly reports", "Jane Smith", "2025-06-20", "Pending", "Waiting for data", "5"],
                ["3", "Update website content", "Bob Johnson", "2025-06-12", "Complete", "Completed ahead of schedule", "3"]
            ]
        elif sheet_name == "KPI_Data":
            return [
                ["Entry ID", "Date", "Employee Name", "Department", "KPI Name", "Target Value", "Actual Value", "Status", "Performance Trend"],
                ["1", "2025-06-01", "John Doe", "Sales", "Sales_Target", "100000", "95000", "Yellow", "Improving"],
                ["2", "2025-06-01", "Jane Smith", "Marketing", "Customer_Satisfaction", "90", "92", "Green", "Stable"],
                ["3", "2025-06-01", "Bob Johnson", "IT", "Project_Completion_Rate", "95", "88", "Red", "Declining"]
            ]
        elif sheet_name == "Team_Members":
            return [
                ["Employee ID", "Name", "Email", "Slack ID", "WhatsApp Number", "Role", "Department"],
                ["1", "John Doe", "john.doe@company.com", "@johndoe", "+1234567890", "Sales Manager", "Sales"],
                ["2", "Jane Smith", "jane.smith@company.com", "@janesmith", "+1234567891", "Marketing Specialist", "Marketing"],
                ["3", "Bob Johnson", "bob.johnson@company.com", "@bobjohnson", "+1234567892", "IT Developer", "IT"]
            ]
        else:
            return []
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks from Master_Tasks sheet."""
        data = self.read_sheet_data("Master_Tasks")
        if not data:
            return []
        
        headers = data[0]
        tasks = []
        for row in data[1:]:
            # Pad row with empty strings if it's shorter than headers
            padded_row = row + [''] * (len(headers) - len(row))
            task = dict(zip(headers, padded_row))
            tasks.append(task)
        
        return tasks
    
    def add_task(self, task_data: Dict[str, Any]) -> bool:
        """Add a new task to Master_Tasks sheet."""
        # Generate new task ID
        existing_tasks = self.get_tasks()
        max_id = max([int(task.get('Task ID', 0)) for task in existing_tasks] + [0])
        new_id = max_id + 1
        
        # Prepare row data
        row_data = [
            str(new_id),
            task_data.get('task_name', ''),
            task_data.get('assigned_to', ''),
            task_data.get('due_date', ''),
            task_data.get('priority', 'Medium'),
            task_data.get('status', 'To Do'),
            task_data.get('frequency', 'One-time'),
            '',  # Completion Timestamp
            task_data.get('suggested_deadline', ''),
            task_data.get('ai_category', '')
        ]
        
        return self.append_sheet_data("Master_Tasks", [row_data])
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """Update task status and completion timestamp if completed."""
        # In a real implementation, you would find the specific row and update it
        # For demo purposes, we'll just return True
        print(f"Mock: Updating task {task_id} status to {status}")
        return True
    
    def get_delegations(self) -> List[Dict[str, Any]]:
        """Get all delegations from Delegation_Tracker sheet."""
        data = self.read_sheet_data("Delegation_Tracker")
        if not data:
            return []
        
        headers = data[0]
        delegations = []
        for row in data[1:]:
            padded_row = row + [''] * (len(headers) - len(row))
            delegation = dict(zip(headers, padded_row))
            delegations.append(delegation)
        
        return delegations
    
    def add_delegation(self, delegation_data: Dict[str, Any]) -> bool:
        """Add a new delegation to Delegation_Tracker sheet."""
        existing_delegations = self.get_delegations()
        max_id = max([int(d.get('Delegation ID', 0)) for d in existing_delegations] + [0])
        new_id = max_id + 1
        
        row_data = [
            str(new_id),
            delegation_data.get('task_delegated', ''),
            delegation_data.get('person_responsible', ''),
            delegation_data.get('deadline', ''),
            delegation_data.get('status', 'Pending'),
            delegation_data.get('feedback', ''),
            delegation_data.get('workload_score', '5')
        ]
        
        return self.append_sheet_data("Delegation_Tracker", [row_data])
    
    def get_kpis(self) -> List[Dict[str, Any]]:
        """Get all KPI data from KPI_Data sheet."""
        data = self.read_sheet_data("KPI_Data")
        if not data:
            return []
        
        headers = data[0]
        kpis = []
        for row in data[1:]:
            padded_row = row + [''] * (len(headers) - len(row))
            kpi = dict(zip(headers, padded_row))
            kpis.append(kpi)
        
        return kpis
    
    def add_kpi_entry(self, kpi_data: Dict[str, Any]) -> bool:
        """Add a new KPI entry to KPI_Data sheet."""
        existing_kpis = self.get_kpis()
        max_id = max([int(k.get('Entry ID', 0)) for k in existing_kpis] + [0])
        new_id = max_id + 1
        
        # Calculate status based on target vs actual
        target = float(kpi_data.get('target_value', 0))
        actual = float(kpi_data.get('actual_value', 0))
        
        if actual >= target * 0.9:
            status = "Green"
        elif actual >= target * 0.7:
            status = "Yellow"
        else:
            status = "Red"
        
        row_data = [
            str(new_id),
            kpi_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            kpi_data.get('employee_name', ''),
            kpi_data.get('department', ''),
            kpi_data.get('kpi_name', ''),
            str(kpi_data.get('target_value', 0)),
            str(kpi_data.get('actual_value', 0)),
            status,
            kpi_data.get('performance_trend', 'Stable')
        ]
        
        return self.append_sheet_data("KPI_Data", [row_data])
    
    def get_team_members(self) -> List[Dict[str, Any]]:
        """Get all team members from Team_Members sheet."""
        data = self.read_sheet_data("Team_Members")
        if not data:
            return []
        
        headers = data[0]
        members = []
        for row in data[1:]:
            padded_row = row + [''] * (len(headers) - len(row))
            member = dict(zip(headers, padded_row))
            members.append(member)
        
        return members

