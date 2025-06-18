import React from 'react';

import { Icon } from '@iconify/react';

import { Product } from '../types/product';

interface ProductCardProps {
  product: Product;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const [isHovered, setIsHovered] = React.useState(false);

  return (
    <div
      className="max-w-xs border border-gray-200 rounded-xl shadow-sm overflow-hidden transition-shadow hover:shadow-md bg-white"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative">
        <img
          src={product.image}
          alt={product.name}
          className="w-full aspect-square object-cover"
        />

        {product.isOrganic && (
          <span className="absolute top-2 left-2 px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase bg-green-500 text-white">
            Orgánico
          </span>
        )}

        {product.isBestSeller && (
          <span className="absolute top-2 right-2 px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase bg-orange-500 text-white">
            Top ventas
          </span>
        )}

        <div
          className={`absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center transition-opacity ${
            isHovered ? "opacity-100" : "opacity-0"
          }`}
        >
          <button className="flex items-center gap-2 px-4 py-2 font-medium rounded-md bg-green-500 text-white hover:bg-green-600 transition-colors">
            Añadir al carrito
            <Icon icon="lucide:shopping-cart" />
          </button>
        </div>
      </div>

      <div className="p-3">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="font-semibold text-lg">{product.name}</h3>
            <p className="text-gray-500 text-sm">{product.unit}</p>
          </div>
          <div className="text-right">
            <p className="font-bold text-lg">${product.price.toFixed(0)}</p>
            {product.originalPrice && (
              <p className="text-gray-400 text-sm line-through">
                ${product.originalPrice.toFixed(0)}
              </p>
            )}
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center pt-0 px-3 pb-3 border-t border-gray-100">
        <div className="flex items-center">
          <Icon
            icon={product.inStock ? "lucide:check-circle" : "lucide:x-circle"}
            className={`w-4 h-4 mr-1 ${
              product.inStock ? "text-green-500" : "text-red-500"
            }`}
          />
          <span
            className={`text-xs ${
              product.inStock ? "text-green-500" : "text-red-500"
            }`}
          >
            {product.inStock ? "En Stock" : "no disponible"}
          </span>
        </div>

        <div className="flex items-center">
          <Icon icon="lucide:truck" className="w-4 h-4 mr-1 text-gray-400" />
          <span className="text-xs text-gray-400">
            {product.freeShipping ? "envío gratis" : "Envío estandar"}
          </span>
        </div>
      </div>
    </div>
  );
};
