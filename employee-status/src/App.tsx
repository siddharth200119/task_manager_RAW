"use client"

import { useState, useEffect } from "react"

interface UserType {
  id: number
  name: string
  role: string
}

interface TimeLog {
  end_time: string
  hours_worked: number
  id: number
  notes: string
  start_time: string
  task_id: number
  user_id: number
}

interface Task {
  id: number
  priority: number
  status: string
  title: string
}

interface UsersResponse {
  count: number
  status: string
  users: UserType[]
}

interface TimeLogsResponse {
  count: number
  status: string
  time_logs: TimeLog[]
}

interface TasksResponse {
  count: number
  status: string
  tasks: Task[]
}

function App() {
  const [users, setUsers] = useState<UserType[]>([])
  const [timeLogs, setTimeLogs] = useState<TimeLog[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [selectedUser, setSelectedUser] = useState<UserType | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState("all")
  const [showModal, setShowModal] = useState(false)
  const [activeDashboardTab, setActiveDashboardTab] = useState("employees")
  const [searchQuery, setSearchQuery] = useState("")
  const [isGridView, setIsGridView] = useState(true)
  const [hoveredUser, setHoveredUser] = useState<number | null>(null)
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc")

  // Theme colors
  const primaryColor = "#ff6600"
  const darkColor = "#000000"

  // Fetch users, time logs, and tasks data
  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      try {
        const base_url = 'http://localhost:7991'
        // In a real application, replace these with actual API endpoints
        const usersResponse = await fetch(`${base_url}/users`);
        const usersData: UsersResponse = await usersResponse.json(); // Parse the JSON response

        const timeLogsResponse = await fetch(`${base_url}/time_logs`);
        const timeLogsData: TimeLogsResponse = await timeLogsResponse.json(); // Parse the JSON response

        const tasksResponse = await fetch(`${base_url}/tasks`);
        const tasksData: TasksResponse = await tasksResponse.json(); // Parse the JSON response
        // Set the users from the API response
        setUsers(usersData.users); // Use the users array from the response
        setTimeLogs(timeLogsData.time_logs); // Keep the mock data for time logs
        setTasks(tasksData.tasks); // Keep the mock data for tasks
      } catch (error) {
        console.error("Error fetching data:", error)
        // Use mock data as fallback
        setUsers(mockUsers)
        setTimeLogs(mockTimeLogs)
        setTasks(mockTasks)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  // Filter users based on active tab
  const filteredUsers = users.filter((user) => {
    // First filter by tab
    const matchesTab = 
      activeTab === "all" || 
      (activeTab === "leads" && user.role.includes("Lead")) ||
      (activeTab === "members" && user.role.includes("Member")) ||
      (activeTab === "admin" && user.role.includes("Admin"))
    
    // Then filter by search query
    const matchesSearch = 
      user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.role.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.id.toString().includes(searchQuery)
    
    return matchesTab && matchesSearch
  })

  // Sort users by name
  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (sortOrder === "asc") {
      return a.name.localeCompare(b.name)
    } else {
      return b.name.localeCompare(a.name)
    }
  })

  // Get time logs for a specific user
  const getUserTimeLogs = (userId: number) => {
    return timeLogs.filter((log) => log.user_id === userId)
  }

  // Format date for display
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  // Handle user card click
  const handleUserClick = (user: UserType) => {
    setSelectedUser(user)
    setShowModal(true)
  }

  // Close modal
  const closeModal = () => {
    setShowModal(false)
    setSelectedUser(null)
  }

  // Get role badge class
  const getRoleBadgeClass = (role: string) => {
    if (role.includes("Lead")) return "bg-black text-orange-500 border border-orange-500"
    if (role.includes("Admin")) return "bg-orange-500 text-black"
    return "bg-gray-800 text-gray-200"
  }

  // Get priority badge class and text
  const getPriorityBadge = (priority: number) => {
    switch (priority) {
      case 3:
        return {
          text: "High",
          class: "bg-red-900 text-red-200 border border-red-700"
        }
      case 2:
        return {
          text: "Medium",
          class: "bg-orange-500 text-black"
        }
      case 1:
        return {
          text: "Low",
          class: "bg-gray-700 text-gray-200 border border-gray-600"
        }
      default:
        return {
          text: "None",
          class: "bg-gray-800 text-gray-400"
        }
    }
  }

  // Get status badge class and formatted text
  const getStatusBadge = (status: string) => {
    switch (status) {
      case "pending":
        return {
          text: "Pending",
          class: "bg-gray-800 text-gray-200 border border-gray-700"
        }
      case "in_progress":
        return {
          text: "In Progress",
          class: "bg-black text-orange-500 border border-orange-500"
        }
      case "completed":
        return {
          text: "Completed",
          class: "bg-green-900 text-green-200 border border-green-700"
        }
      default:
        return {
          text: status.replace("_", " "),
          class: "bg-gray-700 text-gray-300"
        }
    }
  }

  // Add this function to handle search
  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value)
  }

  return (
    <div className="min-h-screen bg-gray-900" style={{ backgroundColor: "#121212" }}>
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8 bg-gradient-to-r from-gray-900 to-gray-800 p-6 rounded-lg shadow-lg border border-gray-800">
          <h1 className="text-4xl font-bold text-white flex items-center">
            Employee <span className="ml-2 bg-clip-text text-transparent bg-gradient-to-r from-orange-500 to-yellow-500">Dashboard</span>
          </h1>
          <p className="mt-2 text-sm text-gray-400">
            View employee information, time logs, and task assignments for your team.
          </p>
          <div className="mt-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="relative w-full sm:w-64">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="text"
                className="block w-full pl-10 pr-3 py-2 border border-gray-700 rounded-md leading-5 bg-gray-800 text-gray-300 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition duration-150 ease-in-out"
                placeholder="Search employees..."
                value={searchQuery}
                onChange={handleSearch}
              />
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setIsGridView(true)}
                className={`p-2 rounded-md ${isGridView ? 'bg-gray-700 text-orange-500' : 'bg-gray-800 text-gray-400'}`}
                title="Grid View"
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </button>
              <button
                onClick={() => setIsGridView(false)}
                className={`p-2 rounded-md ${!isGridView ? 'bg-gray-700 text-orange-500' : 'bg-gray-800 text-gray-400'}`}
                title="List View"
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <button
                onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
                className="p-2 rounded-md bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-orange-500"
                title="Sort by Name"
              >
                {sortOrder === "asc" ? (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4" />
                  </svg>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Main Dashboard Tabs */}
        <div className="border-b border-gray-800 mb-6">
          <nav className="-mb-px flex space-x-8 overflow-x-auto">
            <button
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeDashboardTab === "employees"
                  ? `border-orange-500 text-orange-500`
                  : "border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-700"
              }`}
              onClick={() => setActiveDashboardTab("employees")}
              style={{ borderColor: activeDashboardTab === "employees" ? primaryColor : "transparent", color: activeDashboardTab === "employees" ? primaryColor : "" }}
            >
              Employees
            </button>
            <button
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeDashboardTab === "tasks"
                  ? `border-orange-500 text-orange-500`
                  : "border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-700"
              }`}
              onClick={() => setActiveDashboardTab("tasks")}
              style={{ borderColor: activeDashboardTab === "tasks" ? primaryColor : "transparent", color: activeDashboardTab === "tasks" ? primaryColor : "" }}
            >
              Task Assignments
            </button>
          </nav>
        </div>
        
        {activeDashboardTab === "employees" ? (
          <>
            {/* Employee Filter Tabs */}
            <div className="border-b border-gray-800 mb-6">
              <nav className="-mb-px flex space-x-8 overflow-x-auto">
                <button
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === "all"
                      ? `border-orange-500 text-orange-500`
                      : "border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-700"
                  }`}
                  onClick={() => setActiveTab("all")}
                  style={{ borderColor: activeTab === "all" ? primaryColor : "transparent", color: activeTab === "all" ? primaryColor : "" }}
                >
                  All Employees
                </button>
                <button
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === "leads"
                      ? `border-orange-500 text-orange-500`
                      : "border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-700"
                  }`}
                  onClick={() => setActiveTab("leads")}
                  style={{ borderColor: activeTab === "leads" ? primaryColor : "transparent", color: activeTab === "leads" ? primaryColor : "" }}
                >
                  Team Leads
                </button>
                <button
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === "members"
                      ? `border-orange-500 text-orange-500`
                      : "border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-700"
                  }`}
                  onClick={() => setActiveTab("members")}
                  style={{ borderColor: activeTab === "members" ? primaryColor : "transparent", color: activeTab === "members" ? primaryColor : "" }}
                >
                  Team Members
                </button>
              </nav>
            </div>

            {/* Employee Cards */}
            <div>
              {!isGridView ? (
                // List view
                <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-700">
                      <thead className="bg-gray-900">
                        <tr>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Employee
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Role
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Time Logs
                          </th>
                          <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                            Actions
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-gray-800 divide-y divide-gray-700">
                        {sortedUsers.map((user) => (
                          <tr 
                            key={user.id} 
                            className="hover:bg-gray-700 transition-colors duration-150"
                            onMouseEnter={() => setHoveredUser(user.id)}
                            onMouseLeave={() => setHoveredUser(null)}
                          >
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center">
                                <div className="flex-shrink-0 h-10 w-10 relative">
                                  <div 
                                    className="absolute inset-0 rounded-full flex items-center justify-center text-white text-xl font-semibold transform transition-transform duration-300 ease-in-out"
                                    style={{ 
                                      backgroundColor: primaryColor,
                                      transform: hoveredUser === user.id ? 'scale(1.1)' : 'scale(1)'
                                    }}
                                  >
                                    {user.name.charAt(0)}
                                  </div>
                                </div>
                                <div className="ml-4">
                                  <div className="text-sm font-medium text-white">{user.name}</div>
                                  <div className="text-sm text-gray-400">ID: {user.id}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getRoleBadgeClass(user.role)}`}>
                                {user.role}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                              {getUserTimeLogs(user.id).length} logs
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                              <button 
                                onClick={() => handleUserClick(user)} 
                                className="text-gray-400 hover:text-orange-500 transition-colors duration-150"
                                style={{ color: hoveredUser === user.id ? primaryColor : undefined }}
                              >
                                View Details
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                // Grid view with enhanced cards
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {sortedUsers.map((user) => (
                    <div
                      key={user.id}
                      className="group bg-gray-800 rounded-lg shadow hover:shadow-xl transition-all duration-300 cursor-pointer border border-gray-700 hover:border-orange-500 transform hover:-translate-y-1 overflow-hidden"
                      onClick={() => handleUserClick(user)}
                      onMouseEnter={() => setHoveredUser(user.id)}
                      onMouseLeave={() => setHoveredUser(null)}
                    >
                      <div className="h-2 bg-gradient-to-r from-orange-500 to-orange-700 transform origin-left transition-transform duration-300 ease-out" 
                        style={{ transform: hoveredUser === user.id ? 'scaleX(1)' : 'scaleX(0)' }}
                      />
                      <div className="p-4">
                        <div className="flex justify-between items-start">
                          <div className="flex items-center space-x-4">
                            <div 
                              className="w-12 h-12 rounded-full flex items-center justify-center text-white text-xl font-semibold shadow-lg transform transition-transform duration-300 ease-in-out"
                              style={{ 
                                backgroundColor: primaryColor,
                                transform: hoveredUser === user.id ? 'scale(1.1) rotate(5deg)' : 'scale(1)'
                              }}
                            >
                              {user.name.charAt(0)}
                            </div>
                            <div>
                              <h3 className="text-lg font-medium text-white group-hover:text-orange-500 transition-colors duration-300">{user.name}</h3>
                              <p className="text-sm text-gray-400">ID: {user.id}</p>
                            </div>
                          </div>
                          <span
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleBadgeClass(user.role)}`}
                          >
                            {user.role}
                          </span>
                        </div>
                      </div>
                      <div className="px-4 py-3 border-t border-gray-700 bg-gray-850 flex justify-between items-center">
                        <div className="flex items-center text-sm text-gray-400">
                          <svg
                            className="mr-1.5 h-4 w-4 text-gray-500"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth={2}
                          >
                            <circle cx="12" cy="12" r="10" />
                            <polyline points="12 6 12 12 16 14" />
                          </svg>
                          <span>{getUserTimeLogs(user.id).length} time logs</span>
                        </div>
                        <button 
                          className="text-xs text-gray-400 hover:text-orange-500 transition-colors duration-150 opacity-0 group-hover:opacity-100"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleUserClick(user);
                          }}
                        >
                          View Details →
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        ) : (
          /* Task Assignment View */
          <div>
            <div className="mb-6">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-white">
                  Task <span style={{ color: primaryColor }}>Assignments</span>
                </h2>
                <div className="text-sm text-gray-400">
                  Total Tasks: <span className="font-medium" style={{ color: primaryColor }}>{tasks.length}</span>
                </div>
              </div>
            </div>
            
            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="bg-gray-800 rounded-lg shadow animate-pulse h-16"></div>
                ))}
              </div>
            ) : (
              <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-700">
                    <thead className="bg-gray-900">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                          ID
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                          Title
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                          Priority
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                          Status
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-gray-800 divide-y divide-gray-700">
                      {tasks.map((task) => {
                        const priorityBadge = getPriorityBadge(task.priority);
                        const statusBadge = getStatusBadge(task.status);
                        
                        return (
                          <tr key={task.id} className="hover:bg-gray-700">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">
                              #{task.id}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              {task.title}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${priorityBadge.class}`}>
                                {priorityBadge.text}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${statusBadge.class}`}>
                                {statusBadge.text}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                              <button 
                                className="text-gray-400 hover:text-orange-500 font-medium mr-3"
                                style={{ color: primaryColor }}
                              >
                                Assign
                              </button>
                              <button className="text-gray-400 hover:text-gray-300 font-medium">
                                Details
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Enhanced Time Log Modal */}
        {showModal && selectedUser && (
          <div
            className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 backdrop-blur-sm"
            onClick={closeModal}
          >
            <div
              className="bg-gray-900 rounded-lg shadow-2xl max-w-3xl w-full max-h-[90vh] flex flex-col border border-gray-800 transform transition-all duration-300 ease-out"
              style={{ boxShadow: `0 0 30px rgba(255, 102, 0, 0.2)` }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="px-6 py-4 border-b border-gray-800 flex justify-between items-center bg-gradient-to-r from-gray-900 to-gray-800">
                <h2 className="text-xl font-medium text-white flex items-center">
                  <div 
                    className="w-10 h-10 rounded-full flex items-center justify-center text-white text-xl font-semibold mr-3 shadow-lg"
                    style={{ backgroundColor: primaryColor }}
                  >
                    {selectedUser.name.charAt(0)}
                  </div>
                  <div>
                    <span className="text-white">{selectedUser.name}'s</span>
                    <span className="block text-sm text-gray-400">{selectedUser.role}</span>
                  </div>
                </h2>
                <button 
                  className="text-gray-400 hover:text-orange-500 focus:outline-none transition-colors duration-150" 
                  onClick={closeModal}
                >
                  <span className="sr-only">Close</span>
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="px-6 py-4">
                <h3 className="text-lg font-medium text-white mb-2">
                  Time <span style={{ color: primaryColor }}>Logs</span>
                </h3>
                <div className="text-sm text-gray-400 mb-4">
                  Showing all time entries for this employee
                </div>
              </div>
              
              <div className="px-6 pb-6 overflow-y-auto flex-1">
                <div className="border border-gray-800 rounded-lg overflow-hidden bg-gray-800 shadow-inner">
                  {getUserTimeLogs(selectedUser.id).length > 0 ? (
                    <div className="divide-y divide-gray-700">
                      {getUserTimeLogs(selectedUser.id).map((log, index) => (
                        <div 
                          key={log.id} 
                          className="p-4 bg-gray-850 hover:bg-gray-900 transition-colors duration-150"
                          style={{ 
                            animationDelay: `${index * 0.05}s`,
                            animation: 'fadeIn 0.3s ease-out forwards'
                          }}
                        >
                          <div className="flex justify-between items-start mb-3">
                            <div className="font-medium text-white flex items-center">
                              <svg
                                className="mr-2 h-5 w-5 text-gray-500"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={2}
                              >
                                <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                              </svg>
                              Task <span style={{ color: primaryColor, marginLeft: '4px' }}>#{log.task_id}</span>
                            </div>
                            <span 
                              className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium shadow-sm"
                              style={{ backgroundColor: primaryColor, color: "black" }}
                            >
                              {log.hours_worked} hours
                            </span>
                          </div>

                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm mb-3 bg-gray-800 rounded-lg p-3">
                            <div className="flex items-center text-gray-400">
                              <svg
                                className="mr-1.5 h-4 w-4 text-gray-500"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={2}
                              >
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                                <line x1="16" y1="2" x2="16" y2="6" />
                                <line x1="8" y1="2" x2="8" y2="6" />
                                <line x1="3" y1="10" x2="21" y2="10" />
                              </svg>
                              <span>Start: <span className="text-white">{formatDate(log.start_time)}</span></span>
                            </div>
                            <div className="flex items-center text-gray-400">
                              <svg
                                className="mr-1.5 h-4 w-4 text-gray-500"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={2}
                              >
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                                <line x1="16" y1="2" x2="16" y2="6" />
                                <line x1="8" y1="2" x2="8" y2="6" />
                                <line x1="3" y1="10" x2="21" y2="10" />
                              </svg>
                              <span>End: <span className="text-white">{formatDate(log.end_time)}</span></span>
                            </div>
                          </div>

                          {log.notes && (
                            <div className="mt-3 bg-gray-800 rounded-lg p-3 border-l-2" style={{ borderColor: primaryColor }}>
                              <div className="flex items-start">
                                <svg
                                  className="mr-1.5 h-4 w-4 mt-0.5 text-gray-500"
                                  fill="none"
                                  viewBox="0 0 24 24"
                                  stroke="currentColor"
                                  strokeWidth={2}
                                >
                                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                                  <polyline points="14 2 14 8 20 8" />
                                  <line x1="16" y1="13" x2="8" y2="13" />
                                  <line x1="16" y1="17" x2="8" y2="17" />
                                  <polyline points="10 9 9 9 8 9" />
                                </svg>
                                <div className="text-sm text-gray-300">{log.notes}</div>
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-40 text-center p-4">
                      <svg
                        className="h-12 w-12 text-gray-700 mb-2"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        strokeWidth={1.5}
                      >
                        <circle cx="12" cy="12" r="10" />
                        <polyline points="12 6 12 12 16 14" />
                      </svg>
                      <p className="text-gray-500">No time logs found for this employee</p>
                      <button 
                        className="mt-4 px-4 py-2 bg-gray-800 text-orange-500 rounded-md hover:bg-gray-700 transition-colors duration-150"
                        onClick={closeModal}
                      >
                        Close
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

// Mock data for demonstration
const mockUsers: UserType[] = [
  { id: 1, name: "Siddharth", role: "Team Lead" },
  { id: 2, name: "Keval", role: "Team Lead" },
  { id: 3, name: "Princy", role: "Team Lead" },
  { id: 4, name: "Siddharth", role: "Team Lead" },
  { id: 5, name: "Keval", role: "Team Lead" },
  { id: 6, name: "Princy", role: "Team Lead" },
  { id: 7, name: "Gopi", role: "Team Member" },
  { id: 8, name: "Dinkey", role: "Team Member" },
  { id: 9, name: "Sneha", role: "Team Member" },
  { id: 10, name: "Dhaval", role: "Team Member" },
  { id: 11, name: "Parth Frontend", role: "Team Member" },
  { id: 12, name: "Vivek", role: "Team Member" },
  { id: 23, name: "Poojan", role: "Super Admin" },
]

const mockTimeLogs: TimeLog[] = [
  {
    end_time: "2025-03-15 11:00:00",
    hours_worked: 2.0,
    id: 1,
    notes: "Initial review",
    start_time: "2025-03-15 09:00:00",
    task_id: 2,
    user_id: 2,
  },
  {
    end_time: "2025-03-14 13:00:00",
    hours_worked: 3.0,
    id: 2,
    notes: "Completed draft",
    start_time: "2025-03-14 10:00:00",
    task_id: 3,
    user_id: 3,
  },
  {
    end_time: "2025-03-19 15:34:07",
    hours_worked: 2.0,
    id: 3,
    notes: "working",
    start_time: "2025-03-19 15:34:07",
    task_id: 4,
    user_id: 2,
  },
  {
    end_time: "2025-03-19 15:47:05",
    hours_worked: 3.0,
    id: 4,
    notes: "it's working",
    start_time: "2025-03-19 15:47:05",
    task_id: 5,
    user_id: 3,
  },
  {
    end_time: "2025-03-19 15:51:34",
    hours_worked: 3.0,
    id: 5,
    notes: "",
    start_time: "2025-03-19 15:51:34",
    task_id: 5,
    user_id: 3,
  },
  {
    end_time: "2025-03-20 11:33:46",
    hours_worked: 4.0,
    id: 6,
    notes: "working",
    start_time: "2025-03-20 11:33:46",
    task_id: 8,
    user_id: 2,
  },
  {
    end_time: "2025-03-15 11:00:00",
    hours_worked: 2.0,
    id: 7,
    notes: "Initial review",
    start_time: "2025-03-15 09:00:00",
    task_id: 2,
    user_id: 2,
  },
  {
    end_time: "2025-03-14 13:00:00",
    hours_worked: 3.0,
    id: 8,
    notes: "Completed draft",
    start_time: "2025-03-14 10:00:00",
    task_id: 3,
    user_id: 3,
  },
]

// Mock tasks data
const mockTasks: Task[] = [
  {
    id: 1,
    priority: 3,
    status: "pending",
    title: "Project Plan"
  },
  {
    id: 2,
    priority: 2,
    status: "in_progress",
    title: "Code Review"
  },
  {
    id: 3,
    priority: 1,
    status: "completed",
    title: "Documentation"
  },
  {
    id: 4,
    priority: 1,
    status: "pending",
    title: "Create login page"
  },
  {
    id: 5,
    priority: 1,
    status: "pending",
    title: "Create forgot password"
  },
  {
    id: 6,
    priority: 1,
    status: "pending",
    title: "Registration page"
  },
  {
    id: 7,
    priority: 1,
    status: "pending",
    title: "Websocket"
  },
  {
    id: 8,
    priority: 1,
    status: "pending",
    title: "Browser use"
  },
  {
    id: 9,
    priority: 1,
    status: "pending",
    title: "Deployment"
  },
  {
    id: 10,
    priority: 1,
    status: "pending",
    title: "Node js frontend"
  },
  {
    id: 11,
    priority: 1,
    status: "pending",
    title: "Testing module"
  },
  {
    id: 12,
    priority: 1,
    status: "pending",
    title: "Testing module"
  },
  {
    id: 13,
    priority: 3,
    status: "pending",
    title: "Project Plan"
  },
  {
    id: 14,
    priority: 2,
    status: "in_progress",
    title: "Code Review"
  },
]

export default App