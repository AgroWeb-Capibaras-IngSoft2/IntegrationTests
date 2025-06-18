export interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  originalPrice?: number;
  unit: string;
  image: string;
  isOrganic: boolean;
  isBestSeller: boolean;
  inStock: boolean;
  freeShipping: boolean;
  description?: string;
}
