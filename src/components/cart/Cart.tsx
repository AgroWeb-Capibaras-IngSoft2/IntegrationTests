import React from 'react';
import { Icon } from '@iconify/react';

import Navbar from '../navbar';
import { CartItem } from './CartItem';
import { CartSummary } from './CartSummary';

interface Item {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image: string;
  checked: boolean;
}

const initialCartItems: Item[] = [
  {
    id: 1,
    name: "Router, Access Point, Repetidor, Wds Bridge, Ten...",
    price: 60000,
    quantity: 1,
    image: "https://img.heroui.chat/image/fashion?w=200&h=200&u=1",
    checked: true,
  },
  {
    id: 2,
    name: "Funda Forro Portatil De Lujo",
    price: 43900,
    quantity: 1,
    image: "https://img.heroui.chat/image/fashion?w=200&h=200&u=2",
    checked: true,
  },
];

export default function Cart() {
  const [items, setItems] = React.useState<Item[]>(initialCartItems);

  // Toggle quantity
  const updateQuantity = (id: number, newQuantity: number) => {
    setItems(
      items.map((item) =>
        item.id === id ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  // Remove item
  const removeItem = (id: number) => {
    setItems(items.filter((item) => item.id !== id));
  };

  // Toggle individual checked state
  const updateChecked = (id: number, checked: boolean) => {
    setItems(
      items.map((item) =>
        item.id === id ? { ...item, checked } : item
      )
    );
  };

  // Select / Deselect all
  const allChecked = items.length > 0 && items.every((item) => item.checked);
  const toggleAll = () => {
    setItems(items.map((item) => ({ ...item, checked: !allChecked })));
  };

  // Filter only selected items
  const selectedItems = items.filter((item) => item.checked);

  // Calculate totals
  const productTotal = selectedItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  // Calculate total units
  const unitsCount = selectedItems.reduce(
    (sum, item) => sum + item.quantity,
    0
  );

  // Shipping calculation (e.g., 5 650 c/u)
  const shippingPerItem = 5650;
  const shippingCount = unitsCount;
  const shippingTotal = shippingPerItem * shippingCount;

  return (
    <div className="min-h-screen bg-[#EBEBEB]">
      <Navbar userName={null} />
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row gap-4 p-4 md:p-8">
        <div className="w-full md:w-2/3">
          {/* Card Replacement */}
          <div className="bg-white rounded-lg shadow-md mb-4">
            <div className="p-4">
              <div className="flex items-center mb-4">
                <button
                  onClick={toggleAll}
                  className={`mt-2 flex items-center justify-center w-6 h-6 rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${
                    allChecked
                      ? "bg-green-600 hover:bg-green-700"
                      : "border-2 border-gray-300 hover:border-green-400"
                  }`}
                  aria-label={
                    allChecked
                      ? `Deseleccionar todos los productos`
                      : `Seleccionar todos los productos`
                  }
                >
                  {allChecked && (
                    <Icon icon="lucide:check" className="w-4 h-4 text-white" />
                  )}
                </button>
                <span className="text-sm text-[#333333] ml-2 font-semibold px-2 relative top-[4px]">
                  Todos los productos
                </span>
              </div>
              <hr className="my-4 border-gray-200" />
              {items.map((item) => (
                <CartItem
                  key={item.id}
                  item={item}
                  isChecked={item.checked}
                  updateChecked={updateChecked}
                  updateQuantity={updateQuantity}
                  removeItem={removeItem}
                />
              ))}
            </div>
          </div>

          {/* Free Shipping Card */}
          <div className="bg-white rounded-lg shadow-md">
            <div className="p-4">
              <div className="flex items-center text-[#1bb240]">
                {/* Truck Icon SVG */}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="mr-2 h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path d="M8 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM15 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" />
                  <path d="M3 4a1 1 0 00-1 1v10a1 1 0 001 1h1.05a2.5 2.5 0 014.9 0H10a1 1 0 001-1v-1h4.05a2.5 2.5 0 014.9 0H20a1 1 0 001-1v-4a1 1 0 00-.293-.707l-4-4A1 1 0 0016 4H3z" />
                </svg>
                <span className="font-semibold text-green-500">
                  Envío gratis
                </span>
              </div>
              <p className="text-sm text-[#333333] mt-2">
                Aprovecha tu envío gratis agregando más productos Full.
                <button className="text-green-500 hover:text-green-700 p-0 ml-1 font-medium focus:outline-none">
                  Ver más productos Full
                </button>
              </p>
            </div>
          </div>
        </div>

        <div className="w-full md:w-1/3">
          <CartSummary
            total={productTotal}
            selectedCount={selectedItems.length}
            unitsCount={unitsCount}
            shippingCount={shippingCount}
            shippingTotal={shippingTotal}
          />
        </div>
      </div>
    </div>
  );
}