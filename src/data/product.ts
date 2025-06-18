import { Product } from '../types/product';

export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch('http://127.0.0.1:5000/products');
  if (!response.ok) {
    throw new Error('Error fetching products');
  }
  return await response.json();
}