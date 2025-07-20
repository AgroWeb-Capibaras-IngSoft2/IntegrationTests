import React from "react";

import { Icon } from "@iconify/react";

const vegetables = [
  { name: "Cerezas", sales: 1234, icon: "lucide:cherry" },
  { name: "Zanahoria", sales: 987, icon: "lucide:carrot" },
  { name: "Lechugas", sales: 765, icon: "lucide:leaf" },
  { name: "Naranjas", sales: 543, icon: "lucide:citrus" },
];

export const TopSelling: React.FC = () => {
  const maxSales = Math.max(...vegetables.map((veg) => veg.sales));

  return (
    <div className="border border-gray-200 rounded-xl shadow-sm overflow-hidden">
      {/* Card Header */}
      <div className="px-5 py-4 border-b border-gray-100">
        <h4 className="text-lg font-semibold">Top Ventas del mes</h4>
      </div>

      {/* Card Body */}
      <div className="p-5">
        <div className="space-y-4">
          {vegetables.map((veg) => (
            <div key={veg.name} className="flex items-center gap-4">
              <Icon icon={veg.icon} className="text-2xl text-green-500" />
              <div className="flex-1">
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-semibold">{veg.name}</span>
                  <span className="text-sm text-gray-500">{veg.sales}</span>
                </div>

                {/* Progress Bar */}
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500 rounded-full"
                    style={{ width: `${(veg.sales / maxSales) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
