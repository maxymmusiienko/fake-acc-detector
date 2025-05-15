"use client"

import { useEffect, useState } from "react"
import Link from "next/link"

interface UserStats {
    user_id: number
    message_count: number
    chat_count: number
    chat_names: string[]
}

interface StatsResponse {
    [key: string]: UserStats
}

export default function StatsPage() {
    const [stats, setStats] = useState<StatsResponse | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function fetchStats() {
            try {
                // Assuming the API is running on the same host but different port
                const response = await fetch("http://localhost:8000/stats")

                if (!response.ok) {
                    throw new Error(`Error fetching stats: ${response.status}`)
                }

                const data = await response.json()
                setStats(data)
            } catch (err) {
                setError(err instanceof Error ? err.message : "An error occurred")
                console.error("Failed to fetch stats:", err)
            } finally {
                setLoading(false)
            }
        }

        fetchStats()
    }, [])

    return (
        <div className="min-h-screen p-8">
            <div className="max-w-6xl mx-auto">
                <header className="mb-8">
                    <h1 className="text-3xl font-bold mb-2">Telegram User Stats</h1>
                    <Link href="/" className="text-blue-500 hover:underline">
                        Back to Home
                    </Link>
                </header>

                {loading && (
                    <div className="flex justify-center items-center h-64">
                        <p className="text-lg">Loading stats...</p>
                    </div>
                )}

                {error && (
                    <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                        <p>{error}</p>
                        <p className="text-sm mt-2">Make sure the API server is running on port 8000.</p>
                    </div>
                )}

                {stats && !loading && (
                    <div className="grid gap-6">
                        <p className="text-gray-600">Total users: {Object.keys(stats).length}</p>

                        <div className="overflow-x-auto">
                            <table className="w-full border-collapse">
                                <thead>
                                <tr className="bg-gray-100">
                                    <th className="border px-4 py-2 text-left">User ID</th>
                                    <th className="border px-4 py-2 text-left">Messages</th>
                                    <th className="border px-4 py-2 text-left">Chats</th>
                                    <th className="border px-4 py-2 text-left">Chat Names</th>
                                    <th className="border px-4 py-2 text-left">Actions</th>
                                </tr>
                                </thead>
                                <tbody>
                                {Object.entries(stats).map(([userId, userData]) => (
                                    <tr key={userId} className="hover:bg-gray-50">
                                        <td className="border px-4 py-2">{userData.user_id}</td>
                                        <td className="border px-4 py-2">{userData.message_count}</td>
                                        <td className="border px-4 py-2">{userData.chat_count}</td>
                                        <td className="border px-4 py-2">
                                            <ul className="list-disc list-inside">
                                                {userData.chat_names.map((chatName, index) => (
                                                    <li key={index} className="truncate max-w-xs">
                                                        {chatName}
                                                    </li>
                                                ))}
                                            </ul>
                                        </td>
                                        <td className="border px-4 py-2">
                                            <Link href={`/stats/${userData.user_id}`} className="text-blue-500 hover:underline">
                                                View Details
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
