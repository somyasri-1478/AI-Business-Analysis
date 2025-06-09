// Application Data
const APP_DATA = {
  "users": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "password": "password123",
      "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150",
      "joinDate": "2024-01-15",
      "productivityScore": 85,
      "currentStreak": 12,
      "totalGoals": 24,
      "completedGoals": 18
    }
  ],
  "goals": [
    {
      "id": 1,
      "title": "Complete Product Launch",
      "description": "Finalize all components for Q2 product release",
      "priority": "High",
      "progress": 75,
      "dueDate": "2024-06-15",
      "category": "Work",
      "status": "active"
    },
    {
      "id": 2,
      "title": "Learn React Development",
      "description": "Master React.js for frontend development",
      "priority": "Medium",
      "progress": 45,
      "dueDate": "2024-07-01",
      "category": "Learning",
      "status": "active"
    },
    {
      "id": 3,
      "title": "Exercise Daily",
      "description": "30 minutes of physical activity every day",
      "priority": "High",
      "progress": 60,
      "dueDate": "2024-12-31",
      "category": "Health",
      "status": "active"
    }
  ],
  "tasks": [
    {
      "id": 1,
      "title": "Review user feedback",
      "completed": false,
      "goalId": 1,
      "dueDate": "2024-06-10",
      "priority": "High"
    },
    {
      "id": 2,
      "title": "Update documentation",
      "completed": true,
      "goalId": 1,
      "dueDate": "2024-06-08",
      "priority": "Medium"
    },
    {
      "id": 3,
      "title": "Complete React tutorial",
      "completed": false,
      "goalId": 2,
      "dueDate": "2024-06-12",
      "priority": "Medium"
    }
  ],
  "activityFeed": [
    {
      "id": 1,
      "type": "goal_completed",
      "message": "Completed goal: Weekly Team Sync",
      "timestamp": "2024-06-09T10:30:00Z"
    },
    {
      "id": 2,
      "type": "task_completed",
      "message": "Marked task as complete: Update documentation",
      "timestamp": "2024-06-09T09:15:00Z"
    },
    {
      "id": 3,
      "type": "ai_suggestion",
      "message": "AI Coach suggests: Focus on high-priority tasks this morning",
      "timestamp": "2024-06-09T08:00:00Z"
    }
  ],
  "performanceData": {
    "weeklyProgress": [65, 72, 80, 75, 85, 90, 88],
    "monthlyGoals": [8, 12, 15, 18],
    "focusHours": [6.5, 7.2, 5.8, 8.1, 7.5, 6.9, 7.8]
  },
  "aiCoaching": {
    "dailyMessage": "Great momentum, John! You're 75% through your product launch goal. Consider breaking down the remaining tasks into smaller, manageable chunks.",
    "tips": [
      "Start your day with the most challenging task",
      "Take regular breaks to maintain focus",
      "Celebrate small wins to stay motivated"
    ],
    "suggestions": [
      "Your productivity peaks around 10 AM - schedule important tasks then",
      "Consider delegating some documentation tasks to team members"
    ]
  }
};

// Application State
let currentUser = null;
let isAuthenticated = false;

// Utility Functions
function showLoading() {
  const loadingOverlay = document.getElementById('loading-overlay');
  if (loadingOverlay) {
    loadingOverlay.classList.remove('hidden');
  }
}

function hideLoading() {
  const loadingOverlay = document.getElementById('loading-overlay');
  if (loadingOverlay) {
    loadingOverlay.classList.add('hidden');
  }
}

function showNotification(message, type = 'success') {
  const notificationToast = document.getElementById('notification-toast');
  const notificationMessage = document.getElementById('notification-message');
  
  if (notificationMessage && notificationToast) {
    notificationMessage.textContent = message;
    notificationToast.className = `notification-toast ${type}`;
    notificationToast.classList.remove('hidden');
    
    setTimeout(() => {
      notificationToast.classList.add('hidden');
    }, 3000);
  }
}

function formatTimeAgo(timestamp) {
  const date = new Date(timestamp);
  const now = new Date();
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
  
  if (diffInHours < 1) return 'Just now';
  if (diffInHours < 24) return `${diffInHours}h ago`;
  return `${Math.floor(diffInHours / 24)}d ago`;
}

// Authentication Functions
function initializeAuthTabs() {
  const authTabs = document.querySelectorAll('.auth-tab');
  const authForms = document.querySelectorAll('.auth-form');
  
  authTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const tabName = tab.getAttribute('data-tab');
      
      // Update tab active state
      authTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Update form active state
      authForms.forEach(form => form.classList.remove('active'));
      const targetForm = document.getElementById(`${tabName}-form`);
      if (targetForm) {
        targetForm.classList.add('active');
      }
    });
  });
}

function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validateForm(formData, isSignup = false) {
  const errors = [];
  
  if (isSignup && !formData.name.trim()) {
    errors.push('Name is required');
  }
  
  if (!formData.email.trim()) {
    errors.push('Email is required');
  } else if (!validateEmail(formData.email)) {
    errors.push('Please enter a valid email address');
  }
  
  if (!formData.password.trim()) {
    errors.push('Password is required');
  } else if (formData.password.length < 6) {
    errors.push('Password must be at least 6 characters long');
  }
  
  if (isSignup && formData.password !== formData.confirmPassword) {
    errors.push('Passwords do not match');
  }
  
  return errors;
}

async function handleSignIn(formData) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Check credentials
  const user = APP_DATA.users.find(u => 
    u.email === formData.email && u.password === formData.password
  );
  
  if (user) {
    currentUser = user;
    isAuthenticated = true;
    showDashboard();
    showNotification('Welcome back! Successfully signed in.');
  } else {
    throw new Error('Invalid email or password');
  }
}

async function handleSignUp(formData) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1200));
  
  // Check if user already exists
  const existingUser = APP_DATA.users.find(u => u.email === formData.email);
  if (existingUser) {
    throw new Error('An account with this email already exists');
  }
  
  // Create new user
  const newUser = {
    id: APP_DATA.users.length + 1,
    name: formData.name,
    email: formData.email,
    password: formData.password,
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150",
    joinDate: new Date().toISOString().split('T')[0],
    productivityScore: 0,
    currentStreak: 0,
    totalGoals: 0,
    completedGoals: 0
  };
  
  APP_DATA.users.push(newUser);
  currentUser = newUser;
  isAuthenticated = true;
  showDashboard();
  showNotification('Account created successfully! Welcome to Productivity Beast.');
}

function initializeAuthForms() {
  const signinForm = document.getElementById('signin-form');
  const signupForm = document.getElementById('signup-form');
  
  if (signinForm) {
    signinForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const formData = {
        email: document.getElementById('signin-email').value,
        password: document.getElementById('signin-password').value
      };
      
      const errors = validateForm(formData);
      if (errors.length > 0) {
        showNotification(errors.join(', '), 'error');
        return;
      }
      
      try {
        showLoading();
        await handleSignIn(formData);
      } catch (error) {
        showNotification(error.message, 'error');
      } finally {
        hideLoading();
      }
    });
  }
  
  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const formData = {
        name: document.getElementById('signup-name').value,
        email: document.getElementById('signup-email').value,
        password: document.getElementById('signup-password').value,
        confirmPassword: document.getElementById('confirm-password').value
      };
      
      const errors = validateForm(formData, true);
      if (errors.length > 0) {
        showNotification(errors.join(', '), 'error');
        return;
      }
      
      try {
        showLoading();
        await handleSignUp(formData);
      } catch (error) {
        showNotification(error.message, 'error');
      } finally {
        hideLoading();
      }
    });
  }
}

// Dashboard Functions
function showDashboard() {
  const authPage = document.getElementById('auth-page');
  const dashboardPage = document.getElementById('dashboard-page');
  
  if (authPage && dashboardPage) {
    authPage.classList.add('hidden');
    dashboardPage.classList.remove('hidden');
    populateDashboard();
  }
}

function showAuthPage() {
  const authPage = document.getElementById('auth-page');
  const dashboardPage = document.getElementById('dashboard-page');
  
  if (authPage && dashboardPage) {
    dashboardPage.classList.add('hidden');
    authPage.classList.remove('hidden');
    currentUser = null;
    isAuthenticated = false;
  }
}

function populateDashboard() {
  if (!currentUser) return;
  
  // Update header info
  const welcomeText = document.getElementById('welcome-text');
  const userAvatar = document.getElementById('user-avatar');
  
  if (welcomeText) welcomeText.textContent = `Welcome back, ${currentUser.name}!`;
  if (userAvatar) userAvatar.src = currentUser.avatar;
  
  // Update quick stats
  const activeTasks = APP_DATA.tasks.filter(task => !task.completed);
  const todayTasks = document.getElementById('today-tasks');
  const streakCount = document.getElementById('streak-count');
  const productivityScore = document.getElementById('productivity-score');
  
  if (todayTasks) todayTasks.textContent = activeTasks.length;
  if (streakCount) streakCount.textContent = currentUser.currentStreak;
  if (productivityScore) productivityScore.textContent = currentUser.productivityScore;
  
  // Update active goals count
  const activeGoals = APP_DATA.goals.filter(goal => goal.status === 'active');
  const activeGoalsCount = document.getElementById('active-goals-count');
  if (activeGoalsCount) activeGoalsCount.textContent = activeGoals.length;
  
  // Populate goals list
  populateGoalsList();
  
  // Populate activity feed
  populateActivityFeed();
  
  // Populate AI coaching
  populateAICoaching();
  
  // Initialize weekly chart
  setTimeout(() => initializeWeeklyChart(), 100);
}

function populateGoalsList() {
  const goalsList = document.getElementById('goals-list');
  if (!goalsList) return;
  
  const activeGoals = APP_DATA.goals.filter(goal => goal.status === 'active');
  
  goalsList.innerHTML = activeGoals.map(goal => `
    <div class="goal-item">
      <div class="goal-header">
        <h4 class="goal-title">${goal.title}</h4>
        <span class="goal-priority ${goal.priority.toLowerCase()}">${goal.priority}</span>
      </div>
      <p class="goal-description">${goal.description}</p>
      <div class="goal-progress">
        <div class="progress-bar">
          <div class="progress-fill" style="width: ${goal.progress}%"></div>
        </div>
        <span class="progress-text">${goal.progress}%</span>
      </div>
    </div>
  `).join('');
}

function populateActivityFeed() {
  const activityFeed = document.getElementById('activity-feed');
  if (!activityFeed) return;
  
  activityFeed.innerHTML = APP_DATA.activityFeed.map(activity => `
    <div class="activity-item">
      <div class="activity-icon ${activity.type}">
        ${activity.type === 'goal_completed' ? '🎯' : 
          activity.type === 'task_completed' ? '✅' : '🤖'}
      </div>
      <div class="activity-content">
        <div class="activity-message">${activity.message}</div>
        <div class="activity-time">${formatTimeAgo(activity.timestamp)}</div>
      </div>
    </div>
  `).join('');
}

function populateAICoaching() {
  const dailyMessage = document.getElementById('daily-message');
  const coachTips = document.getElementById('coach-tips');
  
  if (dailyMessage) {
    dailyMessage.innerHTML = `<p>${APP_DATA.aiCoaching.dailyMessage}</p>`;
  }
  
  if (coachTips) {
    coachTips.innerHTML = APP_DATA.aiCoaching.tips.map(tip => `
      <div class="tip-item">💡 ${tip}</div>
    `).join('');
  }
}

function initializeWeeklyChart() {
  const canvas = document.getElementById('weekly-chart');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  const data = APP_DATA.performanceData.weeklyProgress;
  
  // Clear canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  // Chart dimensions
  const chartWidth = canvas.width - 60;
  const chartHeight = canvas.height - 60;
  const startX = 30;
  const startY = 30;
  
  // Draw grid
  ctx.strokeStyle = '#e5e5e5';
  ctx.lineWidth = 1;
  
  // Horizontal lines
  for (let i = 0; i <= 5; i++) {
    const y = startY + (i * chartHeight / 5);
    ctx.beginPath();
    ctx.moveTo(startX, y);
    ctx.lineTo(startX + chartWidth, y);
    ctx.stroke();
  }
  
  // Vertical lines
  for (let i = 0; i <= 6; i++) {
    const x = startX + (i * chartWidth / 6);
    ctx.beginPath();
    ctx.moveTo(x, startY);
    ctx.lineTo(x, startY + chartHeight);
    ctx.stroke();
  }
  
  // Draw line chart
  ctx.strokeStyle = '#21808d';
  ctx.lineWidth = 3;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  
  ctx.beginPath();
  data.forEach((value, index) => {
    const x = startX + (index * chartWidth / 6);
    const y = startY + chartHeight - (value / 100 * chartHeight);
    
    if (index === 0) {
      ctx.moveTo(x, y);
    } else {
      ctx.lineTo(x, y);
    }
  });
  ctx.stroke();
  
  // Draw data points
  ctx.fillStyle = '#21808d';
  data.forEach((value, index) => {
    const x = startX + (index * chartWidth / 6);
    const y = startY + chartHeight - (value / 100 * chartHeight);
    
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fill();
  });
  
  // Draw labels
  ctx.fillStyle = '#626c71';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'center';
  
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  days.forEach((day, index) => {
    const x = startX + (index * chartWidth / 6);
    ctx.fillText(day, x, startY + chartHeight + 20);
  });
}

function initializeNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const contentSections = document.querySelectorAll('.content-section');
  
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      
      const sectionName = item.getAttribute('data-section');
      
      // Update nav active state
      navItems.forEach(nav => nav.classList.remove('active'));
      item.classList.add('active');
      
      // Update content sections
      contentSections.forEach(section => section.classList.remove('active'));
      const targetSection = document.getElementById(`${sectionName}-section`);
      if (targetSection) {
        targetSection.classList.add('active');
      }
    });
  });
}

function initializeLogout() {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      showAuthPage();
      showNotification('Successfully logged out. See you soon!');
    });
  }
}

// Social Login Handlers
function initializeSocialLogin() {
  const socialButtons = document.querySelectorAll('.social-btn');
  socialButtons.forEach(button => {
    button.addEventListener('click', () => {
      const platform = button.textContent.trim();
      showNotification(`${platform} login coming soon!`, 'info');
    });
  });
}

// Quick Action Handlers
function initializeQuickActions() {
  const actionCards = document.querySelectorAll('.action-card');
  actionCards.forEach(card => {
    card.addEventListener('click', () => {
      const actionText = card.querySelector('h3').textContent;
      showNotification(`${actionText} feature coming soon!`, 'info');
    });
  });
}

// Initialize Application
function initializeApp() {
  console.log('Initializing Productivity Beast...');
  
  // Ensure loading overlay is hidden on startup
  hideLoading();
  
  // Initialize all components
  initializeAuthTabs();
  initializeAuthForms();
  initializeNavigation();
  initializeLogout();
  initializeSocialLogin();
  initializeQuickActions();
  
  // Show auth page by default
  showAuthPage();
  
  console.log('Productivity Beast initialized successfully!');
}

// Start the application when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeApp);