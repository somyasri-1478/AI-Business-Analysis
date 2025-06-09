# Google Apps Script Setup Guide for Business Systems AI

This guide will help you set up the Google Apps Script automation for your Business Systems AI dashboard.

## Prerequisites

1. Google account with access to Google Sheets and Google Apps Script
2. A Google Sheets spreadsheet with the following sheets:
   - Master Task Sheet
   - Delegation Tracker
   - KPI Dashboard
   - Team Members
3. (Optional) A Google Drive folder for backups

## Step 1: Prepare Your Google Sheets

### Master Task Sheet Structure
Create a sheet named "Master Task Sheet" with these columns:
- Task ID
- Task Name
- Assigned To
- Due Date
- Priority (High/Medium/Low)
- Status (To Do/In Progress/Done)
- Frequency (One-time/Daily/Weekly/Monthly)
- Completion Timestamp
- AI Category (optional)
- Suggested Deadline (optional)

### Delegation Tracker Structure
Create a sheet named "Delegation Tracker" with these columns:
- Task Delegated
- Person Responsible
- Deadline
- Status (Pending/In Progress/Complete)
- Feedback/Comments
- Workload Score

### KPI Dashboard Structure
Create a sheet named "KPI Dashboard" with these columns:
- Employee Name
- Department
- KPI Name
- Target Value
- Actual Value
- Date
- Status (Green/Yellow/Red)
- Performance Trend

### Team Members Structure
Create a sheet named "Team Members" with these columns:
- Name
- Email
- Department
- Role
- Manager

## Step 2: Set Up Google Apps Script

1. Open Google Apps Script (script.google.com)
2. Click "New Project"
3. Replace the default code with the contents of `BusinessSystemsAutomation.gs`
4. Create additional script files:
   - Click the "+" next to "Files" and add `DataValidationAndBackup.gs`

## Step 3: Configure the Scripts

### Update Configuration Constants

In `BusinessSystemsAutomation.gs`, update these constants:

```javascript
const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'; // Get this from your Google Sheets URL
const API_BASE_URL = 'https://your-api-domain.com/api'; // Your Flask API URL
```

In `DataValidationAndBackup.gs`, update:

```javascript
const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'; // Same as above
const BACKUP_FOLDER_ID = 'YOUR_BACKUP_FOLDER_ID_HERE'; // Optional: Google Drive folder for backups
```

### Get Your Spreadsheet ID

1. Open your Google Sheets document
2. Look at the URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
3. Copy the SPREADSHEET_ID part

### Get Your Backup Folder ID (Optional)

1. Create a folder in Google Drive for backups
2. Open the folder
3. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID`
4. Copy the FOLDER_ID part

## Step 4: Enable Required Services

1. In Google Apps Script, click on "Services" (+ icon)
2. Add these services:
   - Gmail API
   - Google Sheets API
   - Google Drive API

## Step 5: Set Up Triggers

Run the setup function to create automated triggers:

1. In Google Apps Script, select the function `setupAutomation`
2. Click "Run"
3. Grant necessary permissions when prompted
4. Also run `setupValidationAndBackup` for data validation and backup automation

## Step 6: Configure Email Settings

### Update Email Addresses

In the script files, update these email addresses to match your organization:

- `manager@company.com` - Manager email for KPI alerts and reports
- `admin@company.com` - Administrator email for error notifications

### Email Templates

The scripts include built-in email templates for:
- Task assignments
- Daily summaries
- Overdue reminders
- KPI alerts
- Weekly reports
- Error notifications

## Step 7: Test the Automation

### Manual Testing Functions

Use these functions to test individual components:

```javascript
testTaskGeneration()      // Test recurring task generation
testDailySummaries()      // Test daily summary emails
testOverdueReminders()    // Test overdue task reminders
testKPIMonitoring()       // Test KPI monitoring and alerts
testWeeklyReport()        // Test weekly report generation
```

### Data Validation Testing

```javascript
validateDataIntegrity()   // Check data quality
generateDataQualityReport() // Generate validation report
createBackup()           // Create manual backup
```

## Step 8: Monitor and Maintain

### Automation Logs

The scripts create log sheets to track automation activities:
- Automation Log - General automation activities
- Validation Log - Data validation results
- Backup Log - Backup and restore activities

### Scheduled Operations

The automation runs on these schedules:
- **Hourly**: Main automation (task generation, reminders, KPI monitoring)
- **Daily at 9 AM**: Daily task summaries
- **Daily at 8 AM**: Data validation
- **Friday at 5 PM**: Weekly reports
- **Sunday at 2 AM**: Weekly backups

## Troubleshooting

### Common Issues

1. **Permission Errors**: Make sure you've granted all necessary permissions
2. **Email Not Sending**: Check that Gmail API is enabled and email addresses are correct
3. **Sheet Not Found**: Verify sheet names match exactly (case-sensitive)
4. **Trigger Not Running**: Check that triggers are properly set up in the Apps Script dashboard

### Error Notifications

The system automatically sends error notifications to the admin email when issues occur.

### Manual Intervention

If automation fails, you can:
1. Check the automation logs in your spreadsheet
2. Run individual test functions to identify issues
3. Restore from backup if data corruption occurs

## Advanced Configuration

### Custom Email Templates

You can modify the email templates in the script by editing these functions:
- `sendTaskAssignmentNotification()`
- `sendDailySummaryEmail()`
- `sendOverdueReminderEmail()`
- `sendKPIAlertEmail()`
- `sendWeeklyReport()`

### API Integration

To integrate with your Flask API, uncomment and modify the API sync code in the `syncDataWithAPI()` function.

### Custom Validation Rules

Add custom data validation rules in the `setupDataValidationRules()` function.

## Security Considerations

1. **Permissions**: Only grant minimum necessary permissions
2. **Email Addresses**: Verify all email addresses before deployment
3. **API Keys**: If using external APIs, store keys securely
4. **Backup Access**: Limit access to backup folders
5. **Script Access**: Restrict who can modify the Apps Script project

## Support

For issues or questions:
1. Check the automation logs in your spreadsheet
2. Review the Google Apps Script execution transcript
3. Verify all configuration settings
4. Test individual functions manually

## Updates and Maintenance

1. **Regular Backups**: The system creates automatic weekly backups
2. **Log Monitoring**: Review automation logs regularly
3. **Data Quality**: Check data validation reports
4. **Performance**: Monitor script execution times and quotas
5. **Updates**: Keep scripts updated with new features and bug fixes

