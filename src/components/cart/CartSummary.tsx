import React from 'react';

interface CartSummaryProps {
  total: number;
  selectedCount: number;
  unitsCount: number;
  shippingCount: number;
  shippingTotal: number;
}

export const CartSummary: React.FC<CartSummaryProps> = ({
  total,
  selectedCount,
  unitsCount,
  shippingCount,
  shippingTotal,
}) => {
  return (
    <div className="border rounded-lg shadow-sm bg-white">
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-4">Resumen de compra</h2>
        <div className="flex justify-between mb-2">
          <span className="text-sm text-[#333333]">
            Productos ({selectedCount})
          </span>
          <span className="text-sm text-[#333333]">
            $ {total.toLocaleString()}
          </span>
        </div>
        <div className="flex justify-between mb-2">
          <span className="text-sm text-[#333333]">Unidades</span>
          <span className="text-sm text-[#333333]">{unitsCount}</span>
        </div>
        <div className="flex justify-between mb-4">
          <span className="text-sm text-[#333333]">
            Envíos ({shippingCount})
          </span>
          <span className="text-sm text-[#333333]">
            $ {shippingTotal.toLocaleString()}
          </span>
        </div>
        <hr className="border-t border-gray-200 my-4" />
        <div className="flex justify-between mb-4">
          <span className="text-lg font-semibold">Total</span>
          <span className="text-lg font-semibold">
            $ {(total + shippingTotal).toLocaleString()}
          </span>
        </div>
        <button className="relative overflow-hidden w-full py-2 px-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-medium rounded-lg shadow-lg hover:shadow-xl hover:bg-gradient-to-r hover:from-green-600 hover:to-emerald-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2">
          Continuar compra
        </button>
      </div>
    </div>
  );
};