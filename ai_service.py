"""
AI service module for task automation and analytics.
Simplified version for deployment without heavy dependencies.
"""
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
import random


class AITaskAnalyzer:
    """AI service for task analysis and automation."""
    
    def __init__(self):
        # Task categories with keywords
        self.task_categories = {
            'Development': ['code', 'develop', 'build', 'implement', 'program', 'software', 'app', 'website', 'api', 'database', 'frontend', 'backend', 'react', 'javascript', 'python', 'feature'],
            'Marketing': ['marketing', 'campaign', 'social', 'content', 'brand', 'promotion', 'advertising', 'seo', 'email', 'newsletter'],
            'Operations': ['operations', 'process', 'workflow', 'procedure', 'system', 'infrastructure', 'deployment', 'maintenance'],
            'Research': ['research', 'analyze', 'study', 'investigate', 'survey', 'data', 'report', 'findings'],
            'Project Management': ['project', 'manage', 'coordinate', 'plan', 'schedule', 'timeline', 'milestone', 'meeting'],
            'Quality Assurance': ['test', 'quality', 'bug', 'review', 'validation', 'verification', 'qa'],
            'Content Management': ['content', 'write', 'edit', 'publish', 'documentation', 'manual', 'guide'],
            'Analysis': ['analysis', 'metrics', 'performance', 'statistics', 'dashboard', 'kpi', 'insights']
        }
        
        # Priority keywords
        self.priority_keywords = {
            'High': ['urgent', 'critical', 'asap', 'emergency', 'important', 'priority'],
            'Medium': ['moderate', 'normal', 'standard', 'regular'],
            'Low': ['minor', 'low', 'optional', 'nice to have', 'when possible']
        }
        
        # Complexity indicators
        self.complexity_keywords = {
            'High': ['complex', 'advanced', 'sophisticated', 'comprehensive', 'full-scale', 'enterprise'],
            'Medium': ['moderate', 'standard', 'typical', 'regular'],
            'Low': ['simple', 'basic', 'quick', 'minor', 'small']
        }
    
    def categorize_task(self, task_name: str, task_description: str = "") -> Dict[str, Any]:
        """Categorize a task based on its name and description."""
        text = f"{task_name} {task_description}".lower()
        
        # Count keyword matches for each category
        category_scores = {}
        for category, keywords in self.task_categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            category_scores[category] = score
        
        # Find the best matching category
        best_category = max(category_scores, key=category_scores.get)
        best_score = category_scores[best_category]
        
        # Calculate confidence based on keyword matches
        total_words = len(text.split())
        confidence = min(best_score / max(total_words * 0.1, 1), 1.0)
        
        return {
            'category': best_category,
            'confidence': round(confidence, 2),
            'all_scores': category_scores,
            'reasoning': f"Matched {best_score} keywords for {best_category}"
        }
    
    def suggest_deadline(self, task_name: str, task_description: str = "", 
                        priority: str = "Medium", estimated_hours: int = None) -> Dict[str, Any]:
        """Suggest a deadline for a task based on various factors."""
        
        # Analyze task complexity
        text = f"{task_name} {task_description}".lower()
        complexity = self._analyze_complexity(text)
        
        # Base days calculation
        base_days = {
            'High': {'High': 1, 'Medium': 2, 'Low': 3},
            'Medium': {'High': 2, 'Medium': 4, 'Low': 6},
            'Low': {'High': 3, 'Medium': 7, 'Low': 14}
        }
        
        days = base_days[priority][complexity]
        
        # Adjust based on estimated hours if provided
        if estimated_hours:
            # Assume 6 working hours per day
            hours_based_days = max(1, estimated_hours // 6)
            days = max(days, hours_based_days)
        
        # Calculate suggested deadline
        suggested_date = datetime.now() + timedelta(days=days)
        
        return {
            'suggested_deadline': suggested_date.strftime('%Y-%m-%d'),
            'days_from_now': days,
            'reasoning': [
                f"Priority: {priority}",
                f"Complexity: {complexity}",
                f"Estimated duration: {days} days",
                f"Suggested completion: {suggested_date.strftime('%B %d, %Y')}"
            ],
            'confidence': 0.8
        }
    
    def analyze_workload_distribution(self, tasks_data: List[Dict], team_data: List[Dict]) -> Dict[str, Any]:
        """Analyze workload distribution across team members."""
        
        # Count tasks per person
        task_counts = Counter()
        task_priorities = {}
        
        for task in tasks_data:
            assignee = task.get('Assigned To', 'Unassigned')
            if assignee != 'Unassigned':
                task_counts[assignee] += 1
                
                # Weight by priority
                priority = task.get('Priority', 'Medium')
                weight = {'High': 3, 'Medium': 2, 'Low': 1}.get(priority, 2)
                
                if assignee not in task_priorities:
                    task_priorities[assignee] = 0
                task_priorities[assignee] += weight
        
        # Calculate workload analysis
        workload_analysis = {}
        for member in team_data:
            name = member.get('Name', '')
            task_count = task_counts.get(name, 0)
            priority_weight = task_priorities.get(name, 0)
            
            # Calculate capacity (simplified)
            capacity = max(0, 100 - (task_count * 20) - (priority_weight * 5))
            
            status = "Light Load" if task_count <= 2 else "Moderate Load" if task_count <= 4 else "Heavy Load"
            
            workload_analysis[name] = {
                'current_tasks': task_count,
                'priority_weight': priority_weight,
                'capacity_available': capacity,
                'workload_status': status
            }
        
        return {
            'team_analysis': workload_analysis,
            'total_tasks': len(tasks_data),
            'average_tasks_per_person': len(tasks_data) / max(len(team_data), 1),
            'recommendations': self._generate_workload_recommendations(workload_analysis)
        }
    
    def break_down_task(self, task_name: str, task_description: str = "", 
                       estimated_hours: int = 40, team_size: int = 1) -> Dict[str, Any]:
        """Break down a complex task into smaller subtasks."""
        
        # Analyze task category
        category_info = self.categorize_task(task_name, task_description)
        category = category_info['category']
        
        # Generate subtasks based on category
        subtasks = self._generate_subtasks_by_category(category, task_name, estimated_hours, team_size)
        
        return {
            'original_task': task_name,
            'category': category,
            'total_estimated_hours': estimated_hours,
            'team_size': team_size,
            'subtasks': subtasks,
            'execution_plan': self._create_execution_plan(subtasks),
            'dependencies': self._identify_dependencies(subtasks)
        }
    
    def smart_task_assignment(self, task_data: Dict, team_data: List[Dict], 
                            current_tasks: List[Dict]) -> Dict[str, Any]:
        """Intelligently assign tasks to team members."""
        
        task_name = task_data.get('task_name', '')
        task_description = task_data.get('task_description', '')
        required_skills = task_data.get('required_skills', '').lower()
        priority = task_data.get('priority', 'Medium')
        
        # Analyze current workload
        workload_analysis = self.analyze_workload_distribution(current_tasks, team_data)
        
        # Score each team member
        assignment_scores = {}
        for member in team_data:
            name = member.get('Name', '')
            
            # Skill match score (simplified)
            skills = member.get('Skills', '').lower()
            skill_match = self._calculate_skill_match(required_skills, skills)
            
            # Workload score
            workload_info = workload_analysis['team_analysis'].get(name, {})
            capacity = workload_info.get('capacity_available', 50) / 100
            
            # Priority adjustment
            priority_multiplier = {'High': 1.2, 'Medium': 1.0, 'Low': 0.8}.get(priority, 1.0)
            
            # Calculate final score
            final_score = (skill_match * 0.6 + capacity * 0.4) * priority_multiplier
            
            assignment_scores[name] = {
                'score': round(final_score, 2),
                'skill_match': skill_match,
                'capacity': capacity,
                'workload_status': workload_info.get('workload_status', 'Unknown'),
                'current_tasks': workload_info.get('current_tasks', 0)
            }
        
        # Find best assignment
        best_assignee = max(assignment_scores, key=lambda x: assignment_scores[x]['score'])
        best_score = assignment_scores[best_assignee]
        
        # Generate alternatives
        sorted_scores = sorted(assignment_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        alternatives = []
        for name, score_info in sorted_scores[1:3]:  # Top 2 alternatives
            alternatives.append({
                'name': name,
                'workload_status': score_info['workload_status'],
                'current_tasks': score_info['current_tasks'],
                'capacity_available': int(score_info['capacity'] * 100)
            })
        
        return {
            'recommended_assignee': best_assignee,
            'confidence_score': best_score['score'],
            'assignment_reasoning': [
                f"Capacity available: {int(best_score['capacity'] * 100)}%",
                f"Skill match: {int(best_score['skill_match'] * 100)}%",
                f"Current workload: {best_score['workload_status']}",
                f"Final score: {best_score['score']}"
            ],
            'alternative_assignees': alternatives,
            'task_analysis': self.categorize_task(task_name, task_description)
        }
    
    def generate_performance_insights(self, tasks_data: List[Dict], 
                                    kpis_data: List[Dict]) -> Dict[str, Any]:
        """Generate AI-powered performance insights."""
        
        # Task completion analysis
        total_tasks = len(tasks_data)
        completed_tasks = len([t for t in tasks_data if t.get('Status') == 'Done'])
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Overdue analysis
        overdue_tasks = []
        for task in tasks_data:
            if task.get('Status') != 'Done' and task.get('Due Date'):
                try:
                    due_date = datetime.strptime(task['Due Date'], '%Y-%m-%d')
                    if due_date < datetime.now():
                        overdue_tasks.append(task)
                except:
                    pass
        
        # KPI analysis
        kpi_status_counts = Counter(kpi.get('Status', 'Unknown') for kpi in kpis_data)
        underperforming_kpis = kpi_status_counts.get('Red', 0) + kpi_status_counts.get('Yellow', 0)
        
        # Generate insights
        insights = {
            'performance_insights': [],
            'trend_analysis': [],
            'recommendations': [],
            'alerts': []
        }
        
        # Performance insights
        if completion_rate < 70:
            insights['performance_insights'].append(
                f"Low task completion rate of {completion_rate:.1f}% needs attention"
            )
        
        if len(overdue_tasks) > 0:
            insights['alerts'].append(
                f"{len(overdue_tasks)} tasks are overdue and require immediate action"
            )
        
        # Trend analysis
        if underperforming_kpis > 0:
            insights['trend_analysis'].append(
                f"Performance concern: {underperforming_kpis} KPIs are underperforming"
            )
        
        # Recommendations
        insights['recommendations'].extend([
            "Regular team check-ins can help identify bottlenecks early",
            "Consider implementing automated task reminders for better deadline management",
            "Monthly KPI reviews can help maintain performance standards"
        ])
        
        return insights
    
    def _analyze_complexity(self, text: str) -> str:
        """Analyze task complexity based on keywords."""
        complexity_scores = {}
        for complexity, keywords in self.complexity_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            complexity_scores[complexity] = score
        
        if complexity_scores['High'] > 0:
            return 'High'
        elif complexity_scores['Low'] > 0:
            return 'Low'
        else:
            return 'Medium'
    
    def _calculate_skill_match(self, required_skills: str, member_skills: str) -> float:
        """Calculate skill match between required and member skills."""
        if not required_skills or not member_skills:
            return 0.5  # Default moderate match
        
        required = set(required_skills.lower().split())
        available = set(member_skills.lower().split())
        
        if not required:
            return 0.5
        
        matches = len(required.intersection(available))
        return min(matches / len(required), 1.0)
    
    def _generate_subtasks_by_category(self, category: str, task_name: str, 
                                     estimated_hours: int, team_size: int) -> List[Dict]:
        """Generate subtasks based on task category."""
        
        subtask_templates = {
            'Development': [
                'Requirements Analysis and Planning',
                'System Design and Architecture',
                'Frontend Development',
                'Backend Development',
                'Database Design and Implementation',
                'Testing and Quality Assurance',
                'Deployment and Documentation'
            ],
            'Marketing': [
                'Market Research and Analysis',
                'Strategy Development',
                'Content Creation',
                'Campaign Implementation',
                'Performance Monitoring',
                'Optimization and Reporting'
            ],
            'Project Management': [
                'Project Planning and Scope Definition',
                'Resource Allocation',
                'Timeline Development',
                'Risk Assessment',
                'Execution Monitoring',
                'Stakeholder Communication',
                'Project Closure and Review'
            ]
        }
        
        templates = subtask_templates.get(category, [
            'Planning and Analysis',
            'Implementation Phase 1',
            'Implementation Phase 2',
            'Review and Testing',
            'Finalization and Documentation'
        ])
        
        # Distribute hours across subtasks
        hours_per_subtask = estimated_hours // len(templates)
        remaining_hours = estimated_hours % len(templates)
        
        subtasks = []
        for i, template in enumerate(templates):
            hours = hours_per_subtask + (1 if i < remaining_hours else 0)
            subtasks.append({
                'id': i + 1,
                'name': f"{template} - {task_name}",
                'estimated_hours': hours,
                'dependencies': [],
                'can_parallel': i > 1  # First two tasks usually sequential
            })
        
        return subtasks
    
    def _create_execution_plan(self, subtasks: List[Dict]) -> Dict[str, Any]:
        """Create an execution plan for subtasks."""
        total_hours = sum(task['estimated_hours'] for task in subtasks)
        
        # Simple sequential plan
        sequential_days = total_hours // 8  # 8 hours per day
        
        # Parallel execution possibilities
        parallel_tasks = [task for task in subtasks if task.get('can_parallel', False)]
        parallel_savings = len(parallel_tasks) * 0.3  # 30% time savings for parallel tasks
        
        optimized_days = max(1, int(sequential_days - parallel_savings))
        
        return {
            'total_estimated_hours': total_hours,
            'sequential_execution_days': sequential_days,
            'optimized_execution_days': optimized_days,
            'parallel_opportunities': len(parallel_tasks),
            'recommended_approach': 'Parallel execution where possible'
        }
    
    def _identify_dependencies(self, subtasks: List[Dict]) -> List[Dict]:
        """Identify dependencies between subtasks."""
        dependencies = []
        
        for i, task in enumerate(subtasks):
            if i > 0:  # Each task depends on the previous one by default
                dependencies.append({
                    'task_id': task['id'],
                    'depends_on': [subtasks[i-1]['id']],
                    'dependency_type': 'sequential'
                })
        
        return dependencies
    
    def _generate_workload_recommendations(self, workload_analysis: Dict) -> List[str]:
        """Generate workload balancing recommendations."""
        recommendations = []
        
        heavy_load_members = [name for name, info in workload_analysis.items() 
                            if info['workload_status'] == 'Heavy Load']
        light_load_members = [name for name, info in workload_analysis.items() 
                            if info['workload_status'] == 'Light Load']
        
        if heavy_load_members:
            recommendations.append(
                f"Consider redistributing tasks from {', '.join(heavy_load_members)} to balance workload"
            )
        
        if light_load_members:
            recommendations.append(
                f"Team members {', '.join(light_load_members)} have capacity for additional tasks"
            )
        
        if not recommendations:
            recommendations.append("Workload appears well-balanced across the team")
        
        return recommendations

