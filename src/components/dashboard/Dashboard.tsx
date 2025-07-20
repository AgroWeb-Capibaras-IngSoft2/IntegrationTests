import React from "react";

import { Icon } from "@iconify/react";

import { Customer } from "./Customer";
import { Recent } from "./Recent";
import { Sales } from "./Sales";
import { TopSelling } from "./TopSelling";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          <StatCard
            title="Ventas Totales"
            value="$12,345"
            icon="lucide:dollar-sign"
            change={5.2}
          />
          <StatCard
            title="Ordenes"
            value="1,234"
            icon="lucide:shopping-cart"
            change={-2.1}
          />
          <StatCard
            title="Clientes"
            value="5,678"
            icon="lucide:users"
            change={3.7}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <Sales />
          <TopSelling />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Recent />
          <Customer />
        </div>
      </main>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  icon: string;
  change: number;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, change }) => {
  const isPositive = change >= 0;

  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
      <div className="p-6 flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 mb-1">{title}</p>
          <p className="text-2xl font-semibold mb-1">{value}</p>
          <p
            className={`text-sm ${
              isPositive ? "text-green-600" : "text-red-600"
            }`}
          >
            {isPositive ? "↑" : "↓"} {change > 0 ? "+" : ""}
            {change}%
          </p>
        </div>
        <div className="bg-green-100 p-3 rounded-lg">
          <Icon icon={icon} className="text-2xl text-green-600" />
        </div>
      </div>
    </div>
  );
};
