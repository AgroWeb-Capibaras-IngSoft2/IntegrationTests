import React from 'react';
import { Icon } from '@iconify/react';

interface CartItemProps {
  item: {
    id: number;
    name: string;
    price: number;
    quantity: number;
    image: string;
  };
  isChecked: boolean;
  updateChecked: (id: number, checked: boolean) => void;
  updateQuantity: (id: number, quantity: number) => void;
  removeItem: (id: number) => void;
}

export const CartItem: React.FC<CartItemProps> = ({
  item,
  isChecked,
  updateChecked,
  updateQuantity,
  removeItem,
}) => {
  return (
    <div className="flex items-start py-4 border-b border-gray-100 last:border-b-0">
      <button
        onClick={() => updateChecked(item.id, !isChecked)}
        className={`mt-2 flex items-center justify-center w-6 h-6 rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${
          isChecked
            ? "bg-green-600 hover:bg-green-700"
            : "border-2 border-gray-300 hover:border-green-400"
        }`}
        aria-label={isChecked ? `Deselect ${item.name}` : `Select ${item.name}`}
      >
        {isChecked && (
          <Icon icon="lucide:check" className="w-4 h-4 text-white" />
        )}
      </button>

      <div className="flex-grow ml-4">
        <div className="flex items-start">
          <img
            src={item.image}
            alt={item.name}
            className="w-20 h-20 object-cover rounded-xl bg-gray-50 mr-4"
          />
          <div className="flex-grow">
            <h3 className="text-base font-medium text-gray-900">
              {item.name}
            </h3>
            <button
              onClick={() => removeItem(item.id)}
              className="mt-1 text-sm text-green-600 hover:text-green-800 flex items-center p-0 border-none cursor-pointer"
            >
              <Icon icon="lucide:trash-2" className="mr-1.5 w-4 h-4" />
              Eliminar
            </button>
          </div>
        </div>
        <div className="flex justify-between items-center mt-4">
          <div className="flex items-center space-x-3">
            <button
              onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
              className="flex items-center justify-center w-9 h-9 rounded-lg bg-gray-50 hover:bg-green-100 transition-colors duration-200"
            >
              <Icon icon="lucide:minus" className="text-gray-700 w-4 h-4" />
            </button>
            <span className="w-8 text-center text-base font-medium text-gray-900">
              {item.quantity}
            </span>
            <button
              onClick={() => updateQuantity(item.id, item.quantity + 1)}
              className="flex items-center justify-center w-9 h-9 rounded-lg bg-gray-50 hover:bg-green-100 transition-colors duration-200 focus:outline-none"
            >
              <Icon icon="lucide:plus" className="text-gray-700 w-4 h-4" />
            </button>
          </div>
          <p className="text-lg font-bold text-gray-900">
            $ {(item.quantity * item.price).toLocaleString()}{" "}
            <span className="text-sm font-normal text-gray-600">
              ({item.price.toLocaleString()} c/u)
            </span>
          </p>
        </div>
      </div>
    </div>
);
};