import React from 'react';
import { Icon } from '@iconify/react';

import Navbar from '../navbar';
import { CartItem } from './CartItem';
import { CartSummary } from './CartSummary';
import type { CartItem as CartItemBack } from '../../services/cartservices'; 
import { getCarritoItems } from '../../services/cartservices';
import { updateCartItem,removeCartItem } from '../../services/cartservices';
interface Item {
  id: number;
  name: string;
  price: number;
  quantity: number;
  image: string;
  checked: boolean;
}

const transformCartItemToItem=(cartItem:CartItemBack):Item=>({
  id:cartItem.product_id,
  name:cartItem.product_name,
  price:cartItem.total_prod,
  quantity:cartItem.cantidad,
  image:cartItem.image || "/static/default.jpg",
  checked:true
});

export default function Cart() {
  
  //Agregamos los items:
  const [items, setItems] = React.useState<Item[]>([]);
  const[loading,setLoading]=React.useState(true);
  const [error,setError]= React.useState<string | null>(null);

  React.useEffect(()=>{
    const loadCartItems =async()=>{
      try{
        const carritoId=localStorage.getItem('carritoId');
        if(!carritoId){
          setError('No se encontro el carrito del usuario');
          return;
        }
        const backendItems=await getCarritoItems(carritoId);
        const transformedItems= backendItems.map(transformCartItemToItem);
        setItems(transformedItems);
      }catch(error){
        console.error("Error cargando carrito: ",error);
        setError('Error al cargar el carrito');
      }finally{
        setLoading(false);
      }
    };

    loadCartItems();
  },[]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#EBEBEB]">
        <Navbar userName={null} />
        <div className="max-w-7xl mx-auto p-4 md:p-8">
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p>Cargando carrito...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#EBEBEB]">
        <Navbar userName={null} />
        <div className="max-w-7xl mx-auto p-4 md:p-8">
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-red-500">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  // Después del useEffect, agregar esta validación:
if (items.length === 0 && !loading && !error) {
  return (
    <div className="min-h-screen bg-[#EBEBEB]">
      <Navbar userName={null} />
      <div className="max-w-7xl mx-auto p-4 md:p-8">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <Icon icon="lucide:shopping-cart" className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold text-gray-600 mb-2">
            Tu carrito está vacío
          </h3>
          <p className="text-gray-500 mb-6">
            ¡Agrega algunos productos para comenzar a comprar!
          </p>
          <button 
            onClick={() => window.location.href = '/catalog'}
            className="bg-green-500 text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
          >
            Ir al catálogo
          </button>
        </div>
      </div>
    </div>
  );
}

  // Toggle quantity
  const updateQuantity = async(id: number, newQuantity: number) => {
    const carritoId=localStorage.getItem('carritoId');
    if(!carritoId) return;
    try {
      await updateCartItem(carritoId, id.toString(), newQuantity);
      const backendItems = await getCarritoItems(carritoId);
      const transformedItems = backendItems.map(transformCartItemToItem);
      setItems(transformedItems);
  } catch (error) {
    alert('Error actualizando cantidad');
  }
  };

  // Remove item
  const removeItem = async (id: number) => {
  const carritoId = localStorage.getItem('carritoId');
  if (!carritoId) return;
  try {
    await removeCartItem(carritoId, id.toString());
    const backendItems = await getCarritoItems(carritoId);
    const transformedItems = backendItems.map(transformCartItemToItem);
    setItems(transformedItems);
  } catch (error) {
    alert('Error eliminando producto');
  }
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