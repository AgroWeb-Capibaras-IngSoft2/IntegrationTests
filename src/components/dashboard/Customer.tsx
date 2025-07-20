import React from "react";

import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const data = [
  { name: "Comprador", value: 60 },
  { name: "Vendedor", value: 40 },
];

const COLORS = ["#17C964", "#006FEE"];

export const Customer: React.FC = () => {
  return (
    <div className="border border-gray-200 rounded-xl shadow-sm overflow-hidden">
      {/* Card Header */}
      <div className="px-5 py-4 border-b border-gray-100">
        <h4 className="text-lg font-semibold">Tipo de usuario</h4>
      </div>

      {/* Card Body */}
      <div className="p-5">
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
