import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import StatCard from '../components/StatCard';
import ActivityItem from '../components/ActivityItem';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalUsers: 0,
    totalBreeds: 0,
    totalFacts: 0,
    totalVideos: 0,
    recentActivities: [],
    userGrowth: []
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:6543/api/admin/stats');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard title="Total Users" value={stats.totalUsers} icon="👥" />
        <StatCard title="Dog Breeds" value={stats.totalBreeds} icon="🐕" />
        <StatCard title="Dog Facts" value={stats.totalFacts} icon="📝" />
        <StatCard title="Viral Videos" value={stats.totalVideos} icon="🎥" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">User Growth</h2>
          <LineChart width={500} height={300} data={stats.userGrowth}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="users" stroke="#8884d8" />
          </LineChart>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Recent Activities</h2>
          <div className="space-y-4">
            {stats.recentActivities.map((activity) => (
              <ActivityItem key={activity.id} activity={activity} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;