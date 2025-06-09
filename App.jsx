import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts'
import { 
  Activity, 
  Users, 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  TrendingUp,
  Brain,
  Mail,
  Calendar,
  Target,
  BarChart3,
  Settings,
  Plus,
  Filter,
  Search,
  Bell,
  ArrowRight,
  Sparkles,
  Zap,
  Shield,
  Globe,
  Eye,
  EyeOff
} from 'lucide-react'
import './App.css'

// API base URL - automatically detects environment
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api' 
  : '/api'  // Use relative URL for production

// Authentication API functions
const authAPI = {
  signup: async (userData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies for session management
        body: JSON.stringify(userData)
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Signup failed')
      }
      
      return data
    } catch (error) {
      console.error('Signup error:', error)
      throw error
    }
  },

  signin: async (credentials) => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies for session management
        body: JSON.stringify(credentials)
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Signin failed')
      }
      
      return data
    } catch (error) {
      console.error('Signin error:', error)
      throw error
    }
  },

  logout: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/logout`, {
        method: 'POST',
        credentials: 'include'
      })
      
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Logout error:', error)
      throw error
    }
  },

  getProfile: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/profile`, {
        method: 'GET',
        credentials: 'include'
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || 'Failed to get profile')
      }
      
      return data
    } catch (error) {
      console.error('Get profile error:', error)
      throw error
    }
  },

  verifySession: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/verify-session`, {
        method: 'GET',
        credentials: 'include'
      })
      
      const data = await response.json()
      return data
    } catch (error) {
      console.error('Session verification error:', error)
      return { success: false, message: 'Session verification failed' }
    }
  }
}

// Authentication Landing Page Component
function AuthPage({ onLogin }) {
  const [authMode, setAuthMode] = useState('signin') // 'signin', 'signup', 'getstarted'
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: '',
    company: ''
  })

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      if (authMode === 'signup') {
        // Validate password confirmation
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match')
          setLoading(false)
          return
        }

        // Call signup API
        const response = await authAPI.signup({
          email: formData.email,
          password: formData.password,
          confirmPassword: formData.confirmPassword,
          firstName: formData.firstName,
          lastName: formData.lastName,
          company: formData.company
        })

        if (response.success) {
          // Successfully signed up, log the user in
          onLogin(response.user)
        } else {
          setError(response.message || 'Signup failed')
        }
      } else {
        // Sign in mode
        const response = await authAPI.signin({
          email: formData.email,
          password: formData.password
        })

        if (response.success) {
          // Successfully signed in
          onLogin(response.user)
        } else {
          setError(response.message || 'Sign in failed')
        }
      }
    } catch (error) {
      console.error('Authentication error:', error)
      setError(error.message || 'Authentication failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const features = [
    {
      icon: <Brain className="w-6 h-6" />,
      title: "AI-Powered Automation",
      description: "Intelligent task categorization and smart deadline suggestions"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Real-time Analytics",
      description: "Comprehensive KPI tracking and performance insights"
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: "Team Management",
      description: "Smart workload distribution and delegation tracking"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Google Sheets Integration",
      description: "Seamless integration with your existing workflows"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="relative z-10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Business Systems AI
            </span>
          </div>
          
          <div className="flex items-center space-x-4">
            {authMode !== 'signin' && (
              <Button 
                variant="ghost" 
                onClick={() => setAuthMode('signin')}
                className="text-gray-600 hover:text-gray-900"
              >
                Sign In
              </Button>
            )}
            {authMode !== 'signup' && (
              <Button 
                variant="outline" 
                onClick={() => setAuthMode('signup')}
                className="border-blue-200 text-blue-600 hover:bg-blue-50"
              >
                Sign Up
              </Button>
            )}
          </div>
        </div>
      </header>

      <div className="flex min-h-[calc(100vh-80px)]">
        {/* Left Side - Hero Content */}
        <div className="flex-1 flex items-center justify-center px-6 py-12">
          <div className="max-w-lg">
            <div className="text-center mb-8">
              <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium mb-6">
                <Sparkles className="w-4 h-4 mr-2" />
                AI-Powered Business Automation
              </div>
              
              <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">
                Transform Your
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  {" "}Business Operations
                </span>
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Streamline task management, automate workflows, and gain intelligent insights 
                with our AI-powered business systems platform.
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              {features.map((feature, index) => (
                <div key={index} className="flex items-start space-x-3 p-4 bg-white/60 backdrop-blur-sm rounded-lg border border-white/20">
                  <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white">
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-1">{feature.title}</h3>
                    <p className="text-sm text-gray-600">{feature.description}</p>
                  </div>
                </div>
              ))}
            </div>

            {authMode === 'getstarted' && (
              <div className="text-center">
                <Button 
                  onClick={() => setAuthMode('signup')} 
                  size="lg"
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3 rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
                >
                  Get Started Free
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
                <p className="text-sm text-gray-500 mt-3">No credit card required • 14-day free trial</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Side - Authentication Form */}
        <div className="flex-1 flex items-center justify-center px-6 py-12">
          <Card className="w-full max-w-md bg-white/80 backdrop-blur-sm border-white/20 shadow-xl">
            <CardHeader className="text-center pb-6">
              <CardTitle className="text-2xl font-bold text-gray-900">
                {authMode === 'signin' && 'Welcome Back'}
                {authMode === 'signup' && 'Create Account'}
                {authMode === 'getstarted' && 'Get Started'}
              </CardTitle>
              <CardDescription className="text-gray-600">
                {authMode === 'signin' && 'Sign in to your account to continue'}
                {authMode === 'signup' && 'Join thousands of teams already using our platform'}
                {authMode === 'getstarted' && 'Start your journey with Business Systems AI'}
              </CardDescription>
            </CardHeader>

            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                {authMode === 'signup' && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label htmlFor="firstName">First Name</Label>
                        <Input
                          id="firstName"
                          name="firstName"
                          type="text"
                          value={formData.firstName}
                          onChange={handleInputChange}
                          required
                          className="mt-1"
                        />
                      </div>
                      <div>
                        <Label htmlFor="lastName">Last Name</Label>
                        <Input
                          id="lastName"
                          name="lastName"
                          type="text"
                          value={formData.lastName}
                          onChange={handleInputChange}
                          required
                          className="mt-1"
                        />
                      </div>
                    </div>
                    
                    <div>
                      <Label htmlFor="company">Company</Label>
                      <Input
                        id="company"
                        name="company"
                        type="text"
                        value={formData.company}
                        onChange={handleInputChange}
                        required
                        className="mt-1"
                      />
                    </div>
                  </>
                )}

                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="mt-1"
                    placeholder="you@company.com"
                  />
                </div>

                <div>
                  <Label htmlFor="password">Password</Label>
                  <div className="relative mt-1">
                    <Input
                      id="password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      value={formData.password}
                      onChange={handleInputChange}
                      required
                      className="pr-10"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {authMode === 'signup' && (
                  <div>
                    <Label htmlFor="confirmPassword">Confirm Password</Label>
                    <Input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      value={formData.confirmPassword}
                      onChange={handleInputChange}
                      required
                      className="mt-1"
                    />
                  </div>
                )}

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <Button 
                  type="submit" 
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-2 px-4 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      {authMode === 'signin' && 'Signing In...'}
                      {authMode === 'signup' && 'Creating Account...'}
                      {authMode === 'getstarted' && 'Getting Started...'}
                    </div>
                  ) : (
                    <>
                      {authMode === 'signin' && 'Sign In'}
                      {authMode === 'signup' && 'Create Account'}
                      {authMode === 'getstarted' && 'Get Started'}
                    </>
                  )}
                </Button>

                <div className="text-center pt-4">
                  {authMode === 'signin' ? (
                    <p className="text-sm text-gray-600">
                      Don't have an account?{' '}
                      <button
                        type="button"
                        onClick={() => setAuthMode('signup')}
                        className="text-blue-600 hover:text-blue-700 font-medium"
                      >
                        Sign up
                      </button>
                    </p>
                  ) : (
                    <p className="text-sm text-gray-600">
                      Already have an account?{' '}
                      <button
                        type="button"
                        onClick={() => setAuthMode('signin')}
                        className="text-blue-600 hover:text-blue-700 font-medium"
                      >
                        Sign in
                      </button>
                    </p>
                  )}
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Footer */}
      <footer className="px-6 py-4 border-t border-white/20 bg-white/30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-sm text-gray-600">
          <div className="flex items-center space-x-6">
            <span>© 2025 Business Systems AI</span>
            <a href="#" className="hover:text-gray-900">Privacy Policy</a>
            <a href="#" className="hover:text-gray-900">Terms of Service</a>
          </div>
          <div className="flex items-center space-x-4">
            <Shield className="w-4 h-4" />
            <span>Enterprise-grade security</span>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Main Dashboard Component (existing dashboard code)
function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [tasks, setTasks] = useState([])
  const [delegations, setDelegations] = useState([])
  const [kpis, setKpis] = useState([])
  const [workloadAnalysis, setWorkloadAnalysis] = useState(null)
  const [aiInsights, setAiInsights] = useState(null)

  // Fetch data from API
  useEffect(() => {
    fetchTasks()
    fetchDelegations()
    fetchKPIs()
    fetchWorkloadAnalysis()
    fetchAIInsights()
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`)
      const data = await response.json()
      if (data.success) {
        setTasks(data.data)
      }
    } catch (error) {
      console.error('Error fetching tasks:', error)
    }
  }

  const fetchDelegations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/delegations`)
      const data = await response.json()
      if (data.success) {
        setDelegations(data.data)
      }
    } catch (error) {
      console.error('Error fetching delegations:', error)
    }
  }

  const fetchKPIs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/kpis`)
      const data = await response.json()
      if (data.success) {
        setKpis(data.data)
      }
    } catch (error) {
      console.error('Error fetching KPIs:', error)
    }
  }

  const fetchWorkloadAnalysis = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/analyze-workload`)
      const data = await response.json()
      if (data.success) {
        setWorkloadAnalysis(data.data)
      }
    } catch (error) {
      console.error('Error fetching workload analysis:', error)
    }
  }

  const fetchAIInsights = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/generate-insights`)
      const data = await response.json()
      if (data.success) {
        setAiInsights(data.data)
      }
    } catch (error) {
      console.error('Error fetching AI insights:', error)
    }
  }

  // Chart data
  const taskStatusData = [
    { name: 'To Do', value: tasks.filter(t => t.Status === 'To Do').length, color: '#8b5cf6' },
    { name: 'In Progress', value: tasks.filter(t => t.Status === 'In Progress').length, color: '#10b981' },
    { name: 'Done', value: tasks.filter(t => t.Status === 'Done').length, color: '#f59e0b' },
    { name: 'Overdue', value: 0, color: '#ef4444' }
  ]

  const workloadData = workloadAnalysis ? Object.entries(workloadAnalysis.team_analysis).map(([name, data]) => ({
    name: name.split(' ')[0], // First name only for chart
    workload: data.current_tasks * 10 + data.priority_weight
  })) : []

  const kpiStatusData = [
    { name: 'Green', value: kpis.filter(k => k.Status === 'Green').length, color: '#10b981' },
    { name: 'Yellow', value: kpis.filter(k => k.Status === 'Yellow').length, color: '#f59e0b' },
    { name: 'Red', value: kpis.filter(k => k.Status === 'Red').length, color: '#ef4444' }
  ]

  const sendTestEmail = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/notifications/test-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: 'test@example.com',
          name: 'Test User'
        })
      })
      const data = await response.json()
      if (data.success) {
        alert('Test email sent successfully!')
      }
    } catch (error) {
      console.error('Error sending test email:', error)
      alert('Error sending test email')
    }
  }

  const sendDailySummary = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/notifications/send-daily-summary`, {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        alert(`Daily summaries sent to ${data.data.emails_sent} employees`)
      }
    } catch (error) {
      console.error('Error sending daily summary:', error)
      alert('Error sending daily summary')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">Business Systems AI</h1>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <span>Welcome, {user.firstName} {user.lastName}</span>
              <span className="text-gray-400">•</span>
              <span>{user.company}</span>
            </div>
            <Button variant="ghost" size="sm">
              <Bell className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="sm" onClick={onLogout}>
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200 px-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-6 bg-transparent border-b-0 h-auto p-0">
            <TabsTrigger 
              value="dashboard" 
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-blue-500 rounded-none py-4 px-6"
            >
              <BarChart3 className="w-4 h-4 mr-2" />
              Dashboard
            </TabsTrigger>
            <TabsTrigger 
              value="tasks"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-purple-500 rounded-none py-4 px-6"
            >
              <CheckCircle className="w-4 h-4 mr-2" />
              Tasks
            </TabsTrigger>
            <TabsTrigger 
              value="delegations"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-green-500 rounded-none py-4 px-6"
            >
              <Users className="w-4 h-4 mr-2" />
              Delegations
            </TabsTrigger>
            <TabsTrigger 
              value="kpis"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-pink-500 rounded-none py-4 px-6"
            >
              <Target className="w-4 h-4 mr-2" />
              KPIs
            </TabsTrigger>
            <TabsTrigger 
              value="ai-insights"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-indigo-500 rounded-none py-4 px-6"
            >
              <Brain className="w-4 h-4 mr-2" />
              AI Insights
            </TabsTrigger>
            <TabsTrigger 
              value="notifications"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-orange-500 rounded-none py-4 px-6"
            >
              <Mail className="w-4 h-4 mr-2" />
              Notifications
            </TabsTrigger>
          </TabsList>

          {/* Dashboard Tab Content */}
          <TabsContent value="dashboard" className="mt-6 space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
                  <CheckCircle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{tasks.length}</div>
                  <p className="text-xs text-muted-foreground">
                    {tasks.filter(t => t.Status === 'Done').length} completed
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Delegations</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{delegations.length}</div>
                  <p className="text-xs text-muted-foreground">
                    {delegations.filter(d => d.Status === 'Complete').length} completed
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">KPI Performance</CardTitle>
                  <Target className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{kpis.filter(k => k.Status === 'Green').length}</div>
                  <p className="text-xs text-muted-foreground">
                    Green status KPIs
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Overdue Tasks</CardTitle>
                  <AlertTriangle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">0</div>
                  <p className="text-xs text-muted-foreground">
                    Need immediate attention
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Task Status Distribution</CardTitle>
                  <CardDescription>Overview of all task statuses</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={taskStatusData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {taskStatusData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Team Workload Analysis</CardTitle>
                  <CardDescription>Current workload distribution across team members</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={workloadData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="workload" fill="#8b5cf6" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            {/* AI Insights */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="w-5 h-5 mr-2" />
                  AI-Generated Insights
                </CardTitle>
                <CardDescription>Intelligent analysis of your business performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Performance Insights</h4>
                    <div className="space-y-2">
                      {aiInsights?.performance_insights?.map((insight, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <TrendingUp className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-600">{insight}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Recommendations</h4>
                    <div className="space-y-2">
                      {aiInsights?.recommendations?.map((rec, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <CheckCircle className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-600">{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tasks Tab Content */}
          <TabsContent value="tasks" className="mt-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Task Management</h2>
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm">
                  <Filter className="w-4 h-4 mr-2" />
                  Filter
                </Button>
                <Button size="sm" className="bg-red-600 hover:bg-red-700">
                  <Plus className="w-4 h-4 mr-2" />
                  New Task
                </Button>
              </div>
            </div>

            <div className="space-y-4">
              {tasks.map((task, index) => (
                <Card key={index}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-2">{task['Task Name']}</h3>
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>Assigned to: {task['Assigned To']}</span>
                          <span>Due: {task['Due Date']}</span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant={task.Priority === 'High' ? 'destructive' : task.Priority === 'Medium' ? 'default' : 'secondary'}>
                          {task.Priority}
                        </Badge>
                        <Badge variant={task.Status === 'Done' ? 'default' : task.Status === 'In Progress' ? 'secondary' : 'outline'}>
                          {task.Status}
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Delegations Tab Content */}
          <TabsContent value="delegations" className="mt-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Delegation Tracking</h2>
              <Button size="sm" className="bg-green-600 hover:bg-green-700">
                <Plus className="w-4 h-4 mr-2" />
                New Delegation
              </Button>
            </div>

            <div className="space-y-4">
              {delegations.map((delegation, index) => (
                <Card key={index}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-2">{delegation['Task Delegated']}</h3>
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span>Responsible: {delegation['Person Responsible']}</span>
                          <span>Deadline: {delegation.Deadline}</span>
                        </div>
                        <p className="text-sm text-gray-500 mt-2">{delegation['Feedback/Comments']}</p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant={delegation.Status === 'Complete' ? 'default' : delegation.Status === 'In Progress' ? 'secondary' : 'outline'}>
                          {delegation.Status}
                        </Badge>
                        <span className="text-sm text-gray-500">Workload: {delegation['Workload Score']}</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* KPIs Tab Content */}
          <TabsContent value="kpis" className="mt-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">KPI Dashboard</h2>
              <Button size="sm" className="bg-pink-600 hover:bg-pink-700">
                <Plus className="w-4 h-4 mr-2" />
                Add KPI Entry
              </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <Card>
                <CardHeader>
                  <CardTitle>KPI Status Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={kpiStatusData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {kpiStatusData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent KPI Entries</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {kpis.slice(0, 3).map((kpi, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <h4 className="font-medium text-gray-900">{kpi['KPI Name']}</h4>
                          <p className="text-sm text-gray-600">{kpi['Employee Name']} - {kpi.Department}</p>
                          <p className="text-sm text-gray-500">{kpi['Actual Value']} / {kpi['Target Value']}</p>
                        </div>
                        <Badge variant={kpi.Status === 'Green' ? 'default' : kpi.Status === 'Yellow' ? 'secondary' : 'destructive'}>
                          {kpi.Status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* AI Insights Tab Content */}
          <TabsContent value="ai-insights" className="mt-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">AI Insights & Analytics</h2>
              <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700">
                <Brain className="w-4 h-4 mr-2" />
                Generate New Insights
              </Button>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Performance Analysis</CardTitle>
                <CardDescription>AI-powered insights into team and project performance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Performance Insights</h4>
                    <div className="space-y-2">
                      {aiInsights?.performance_insights?.map((insight, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <TrendingUp className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-600">{insight}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Trend Analysis</h4>
                    <div className="space-y-2">
                      {aiInsights?.trend_analysis?.map((trend, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <BarChart3 className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-600">{trend}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Recommendations</h4>
                    <div className="space-y-2">
                      {aiInsights?.recommendations?.map((rec, index) => (
                        <div key={index} className="flex items-start space-x-2">
                          <CheckCircle className="w-4 h-4 text-purple-500 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-600">{rec}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Notifications Tab Content */}
          <TabsContent value="notifications" className="mt-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Notification Center</h2>
              <Button size="sm" className="bg-green-600 hover:bg-green-700" onClick={sendTestEmail}>
                <Mail className="w-4 h-4 mr-2" />
                Send Test Email
              </Button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Email Notifications</CardTitle>
                  <CardDescription>Manage automated email notifications</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Button onClick={sendDailySummary} className="w-full justify-start bg-red-50 text-red-700 hover:bg-red-100 border border-red-200">
                    <Mail className="w-4 h-4 mr-2" />
                    Send Daily Task Summary
                  </Button>
                  <Button className="w-full justify-start bg-yellow-50 text-yellow-700 hover:bg-yellow-100 border border-yellow-200">
                    <AlertTriangle className="w-4 h-4 mr-2" />
                    Send Overdue Reminders
                  </Button>
                  <Button className="w-full justify-start bg-red-50 text-red-700 hover:bg-red-100 border border-red-200">
                    <Target className="w-4 h-4 mr-2" />
                    Send KPI Alerts
                  </Button>
                  <Button className="w-full justify-start bg-green-50 text-green-700 hover:bg-green-100 border border-green-200">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Send Weekly Report
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Notification Settings</CardTitle>
                  <CardDescription>Configure automated notification schedules</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="dailySummaryTime" className="text-sm font-medium text-blue-700">
                      Daily Summary Time
                    </Label>
                    <select id="dailySummaryTime" className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-yellow-50">
                      <option>09:00 AM</option>
                      <option>10:00 AM</option>
                      <option>11:00 AM</option>
                    </select>
                  </div>
                  
                  <div>
                    <Label htmlFor="weeklyReportDay" className="text-sm font-medium text-purple-700">
                      Weekly Report Day
                    </Label>
                    <select id="weeklyReportDay" className="w-full mt-1 p-2 border border-gray-300 rounded-md bg-teal-50">
                      <option>Friday</option>
                      <option>Monday</option>
                      <option>Sunday</option>
                    </select>
                  </div>
                  
                  <Button className="w-full bg-gray-800 hover:bg-gray-900 text-white">
                    Save Settings
                  </Button>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

// Main App Component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Check for existing session on app startup
  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await authAPI.verifySession()
        if (response.success && response.user) {
          setUser(response.user)
          setIsAuthenticated(true)
        }
      } catch (error) {
        console.error('Session check error:', error)
        // User is not authenticated, which is fine
      } finally {
        setLoading(false)
      }
    }

    checkSession()
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
    setIsAuthenticated(true)
  }

  const handleLogout = async () => {
    try {
      // Call logout API to clear server-side session
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
      // Continue with logout even if API call fails
    } finally {
      // Clear local state
      setUser(null)
      setIsAuthenticated(false)
    }
  }

  // Show loading screen while checking session
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <AuthPage onLogin={handleLogin} />
  }

  return <Dashboard user={user} onLogout={handleLogout} />
}

export default App

