const ActivityItem = ({ activity }) => {
  return (
    <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
      <div className="flex-shrink-0 text-2xl">{activity.icon}</div>
      <div>
        <p className="font-medium">{activity.description}</p>
        <p className="text-sm text-gray-500">
          {new Date(activity.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default ActivityItem;