const cartApiUrl= import.meta.env.VITE_API_CARRITO_URL || 'http://localhost:5003';
export interface CartItem {
    product_id: number;
    product_name: string;
    cantidad: number;
    medida: string;
    total_prod: number;
}


export interface AddToCartRequest{
    productId:string;
    quantity:number;
}

export interface UpdateCartItemRequest{
    quantity:number
    productId:string;
}

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
        return data.carrito.items || [];
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

// ✅ NUEVA VERSIÓN CON DEBUG:
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