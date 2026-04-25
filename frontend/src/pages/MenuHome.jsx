import { Link } from "react-router-dom";

export default function MenuHome() {
  const role = localStorage.getItem("role") || "buyer";

  const Card = ({ title, description, to }) => (
    <Link
      to={to}
      className="card hover:shadow-lg transition border border-gray-200"
    >
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </Link>
  );

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-6">
        Quick Menu
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Dashboard */}
        <Card
          title="Purchase Order Dashboard"
          description="View and track all purchase orders and their statuses."
          to="/po-dashboard"
        />

        {/* Vendors */}
        {role === "admin" && (
          <Card
            title="Vendors"
            description="Manage vendors and supplier details."
            to="/vendors"
          />
        )}

        {/* Create PO */}
        {role === "admin" && (
          <Card
            title="Create Purchase Order"
            description="Create new purchase orders for approved vendors."
            to="/create-po"
          />
        )}

        {/* AI Agent */}
        <Card
          title="AI Procurement Agent"
          description="Ask questions about vendors, POs, and procurement data."
          to="/agent"
        />
      </div>
    </div>
  );
}
