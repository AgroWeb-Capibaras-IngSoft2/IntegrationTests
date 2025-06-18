export interface Product {
  productId: string;
  name: string;
  category: string;
  price: number;
  originalPrice?: number; // Optional, for products on sale
  unit: string;
  imageUrl: string;
  stock: number;
  origin: string;
  description: string;
  createdAt: string;
  updatedAt: string;
  isActive: boolean;

  // Frontend-only fields (optional, for UI logic)
  isOrganic?: boolean;
  isBestSeller?: boolean;
  inStock: boolean;
  freeShipping: boolean;
}