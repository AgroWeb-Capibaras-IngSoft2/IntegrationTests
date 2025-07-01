import type { Product } from '../types/product';

const apiUrl = import.meta.env.VITE_API_PRODUCTS_URL;

export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch(`${apiUrl}/products`);
  if (!response.ok) {
    throw new Error('Error fetching products');
  }
  return await response.json();
}
