"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useParams } from "next/navigation"

interface Message {
    text: string
    date: string
    chat_name: string
}

interface UserStatsDetailed {
    user_id: number
    message_count: number
    chat_count: number
    chat_names: string[]
    recent_messages: Message[]
}

export default function UserDetailPage() {
    const params = useParams()
    const userId = params.id

    const [stats, setStats] = useState<UserStatsDetailed | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function fetchUserStats() {
            try {
                const response = await fetch(`http://localhost:8000/stats/${userId}`)

                if (!response.ok) {
                    throw new Error(`Error fetching user stats: ${response.status}`)
                }

                const data = await response.json()
                setStats(data)
            } catch (err) {
                setError(err instanceof Error ? err.message : "An error occurred")
                console.error("Failed to fetch user stats:", err)
            } finally {
                setLoading(false)
            }
        }

        if (userId) {
            fetchUserStats()
        }
    }, [userId])

    // Format date to a more readable format
    const formatDate = (dateString: string) => {
        const date = new Date(dateString)
        return new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        }).format(date)
    }

    return (
        <div className="min-h-screen p-8">
            <div className="max-w-6xl mx-auto">
                <header className="mb-8">
                    <div className="flex items-center gap-4 mb-4">
                        <Link href="/stats" className="text-blue-500 hover:underline flex items-center">
                            ← Back to All Users
                        </Link>
                    </div>
                    <h1 className="text-3xl font-bold">User Details</h1>
                </header>

                {loading && (
                    <div className="flex justify-center items-center h-64">
                        <p className="text-lg">Loading user data...</p>
                    </div>
                )}

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                        <p>{error}</p>
                        <p className="text-sm mt-2">Make sure the API server is running on port 8000.</p>
                    </div>
                )}

                {stats && !loading && (
                    <div className="space-y-8">
                        {/* User Summary Card */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                            <h2 className="text-xl font-semibold mb-4">User #{stats.user_id}</h2>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded">
                                    <p className="text-sm text-gray-500 dark:text-gray-400">Total Messages</p>
                                    <p className="text-2xl font-bold">{stats.message_count}</p>
                                </div>

                                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded">
                                    <p className="text-sm text-gray-500 dark:text-gray-400">Active Chats</p>
                                    <p className="text-2xl font-bold">{stats.chat_count}</p>
                                </div>

                                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded">
                                    <p className="text-sm text-gray-500 dark:text-gray-400">Recent Activity</p>
                                    <p className="text-2xl font-bold">
                                        {stats.recent_messages.length > 0
                                            ? formatDate(stats.recent_messages[0].date).split(",")[0]
                                            : "No activity"}
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Chat Names Section */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                            <h2 className="text-xl font-semibold mb-4">Active Chats</h2>

                            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                                {stats.chat_names.map((chatName, index) => (
                                    <div key={index} className="bg-gray-50 dark:bg-gray-700 p-3 rounded flex items-center">
                                        <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                                        <span className="truncate">{chatName}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Recent Messages Section */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                            <h2 className="text-xl font-semibold mb-4">Recent Messages</h2>

                            {stats.recent_messages.length === 0 ? (
                                <p className="text-gray-500">No recent messages found.</p>
                            ) : (
                                <div className="space-y-4">
                                    {stats.recent_messages.map((message, index) => (
                                        <div key={index} className="border-b border-gray-200 dark:border-gray-700 pb-4 last:border-0">
                                            <div className="flex justify-between items-start mb-2">
                                                <span className="font-medium text-blue-600 dark:text-blue-400">{message.chat_name}</span>
                                                <span className="text-xs text-gray-500">{formatDate(message.date)}</span>
                                            </div>
                                            <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line">{message.text}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
