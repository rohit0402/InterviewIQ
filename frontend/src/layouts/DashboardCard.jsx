function DashboardCard({
  title,
  value,
  subtitle,
  icon: Icon,
  color = "blue",
}) {
  const colors = {
    blue: "bg-blue-100 text-blue-600",
    green: "bg-green-100 text-green-600",
    purple: "bg-purple-100 text-purple-600",
    red: "bg-red-100 text-red-600",
  };

  return (
    <div className="rounded-xl bg-white p-6 shadow-sm border hover:shadow-md transition">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>

          <h2 className="mt-2 text-3xl font-bold">{value}</h2>

          {subtitle && (
            <p className="mt-1 text-sm text-gray-400">{subtitle}</p>
          )}
        </div>

        {Icon && (
          <div className={`rounded-xl p-3 ${colors[color]}`}>
            <Icon size={28} />
          </div>
        )}
      </div>
    </div>
  );
}

export default DashboardCard;