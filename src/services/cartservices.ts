const cartApiUrl= import.meta.env.VITE_API_CARRITO_URL || 'http://localhost:5003';
const productApiUrl=import.meta.env.VITE_API_PRODUCTS_URL || 'http://localhost:5000';
export interface CartItem {
    product_id: number;
    product_name: string;
    cantidad: number;
    medida: string;
    total_prod: number;
    image:string;
}


export interface AddToCartRequest{
    productId:string;
    quantity:number;
}

export interface UpdateCartItemRequest{
    quantity:number
    productId:string;
}

const getProductImage = async (product_id:string):Promise<string> =>{
    try{
        const repsonse= await fetch(`${productApiUrl}/products/${product_id}`)
        if(!repsonse.ok){
            console.warn(`No se pudo obtener imagen para producto ${product_id}`);
            return "/static/default.jpg";
        }

        const product=await repsonse.json();
        return product.imageUrl || "static/default.jpg"; 
    }catch(error){
        console.warn(`Error obteniendo imagen para producto ${product_id}:`, error);
        return "/static/default.jpg";
    }
};

export const getCarritoItems=async (carritoId:string):Promise<CartItem[]>=>{
    try
    {
        const response =await fetch (`${cartApiUrl}/carrito/getCarrito/${carritoId}`,{
            method:'GET',
            headers:{
                'Content-Type': 'application/json',
            }
        });

        if(!response.ok){
            throw new Error (`Error ${response.status}: ${response.statusText}`);
        }

        const data= await response.json();
        console.log('Backend repsonse: ',data)
        const items= data.resul.items || [];

        //Obtener imagenes para cada item
        const itemsWithImages=await Promise.all(
            items.map(async (item:any)=>({
                ...item,
                image: await getProductImage(item.product_id)
            }))
        );

        return itemsWithImages;
    } catch(error){
        console.error('Error fetching cart items:',error);
        throw error;
    }
};

//Agregar Producto al carrito
export const addProduct= async(carrito_id:string,productId:string,quantity:number=1): Promise<CartItem>=>{
    try{
        const response=await fetch (`${cartApiUrl}/carrito/addProduct`,{
            method:'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body:JSON.stringify({
                "id_carrito":carrito_id,
                "product_id":productId,
                "cantidad":quantity
            })
        });

        if(!response.ok){
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        const result=await response.json();
        console.log('Backend response: ', result);
        return result;
    }catch (error){
        console.error('Error añadiendo este producto al carrito: ',error)
        throw error;
    }
};

export const crearCarrito = async (userdocument:string,userdocType:string): Promise<{id_carrito:string}>=>{
    try{
        const response=await fetch(`${cartApiUrl}/carrito/create`,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
            },
            body:JSON.stringify({
                "userDocument":userdocument,
                "docType":userdocType
            })
        });

        if(!response.ok){
            throw new Error(`Error ${response.status}: ${response.statusText}`)
        }

        return await response.json();
    }catch(error){
        console.error("Error creando el carrito",error);
        throw error;
    }
};


export const getCarritoIdByUser = async (userdocument: string, docType: string): Promise<string> => {
    try {
        const url = `${cartApiUrl}/carrito/getIdCarrito/${userdocument}/${docType}`;
        console.log('🔍 URL enviada:', url);
        console.log('📋 Parámetros:', { userdocument, docType });
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        console.log('📡 Response status:', response.status);
        console.log('📡 Response ok:', response.ok);

        if (!response.ok) {
            const errorData = await response.json();
            console.log('❌ Error data:', errorData);
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('✅ Success data:', data);
        return data.id_carrito.toString();

    } catch (error) {
        console.error("Error obteniendo el id del carrito", error);
        throw error;
    }
};

export const updateCartItem = async(carritoId:string,product_id:string,newQuantity: number)=>{
    try{
        const response = await fetch(`${cartApiUrl}/carrito/changeQuantity`,{
            method:'PUT',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
                "id_carrito":carritoId,
                "product_id":product_id,
                "cantidad":newQuantity
            })
        });
        if (!response.ok) throw new Error('Error actualizando cantidad');
        return await response.json()
    }catch(error){
        console.error("Error actualizando cantidad: ", error);
        throw error;
    }
};

export const removeCartItem = async (carritoId: string, productId: string) => {
  try {
    const response = await fetch(`${cartApiUrl}/carrito/deleteProduct`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "carrito_id": carritoId,
        "product_id": productId
      })
    });
    if (!response.ok) throw new Error('Error eliminando producto');
    return await response.json();
  } catch (error) {
    console.error('Error eliminando producto:', error);
    throw error;
  }
};