import { Link, useLocation } from 'react-router-dom';

const AdminSidebar = () => {
  const location = useLocation();
    const menuItems = [
    { path: '/admin/facts', label: 'Dog Facts', icon: '📝' },
    { path: '/admin/videos', label: 'Viral Videos', icon: '🎥' },
  ];

  return (
    <div className="w-64 bg-gray-800 text-white min-h-screen">
      <div className="p-4">
        <h2 className="text-2xl font-bold">WoofWorld Admin</h2>
      </div>
      <nav className="mt-8">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center px-6 py-3 ${
              location.pathname === item.path
                ? 'bg-blue-600'
                : 'hover:bg-gray-700'
            }`}
          >
            <span className="mr-3">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
    </div>
  );
};

export default AdminSidebar;