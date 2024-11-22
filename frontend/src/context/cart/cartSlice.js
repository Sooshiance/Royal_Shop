import { createSlice } from '@reduxjs/toolkit';

const loadCartFromLocalStorage = () => {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : { products: [] };
};

const saveCartToLocalStorage = (cart) => {
    localStorage.setItem('cart', JSON.stringify(cart));
};

const cartSlice = createSlice({
    name: 'cart',
    initialState: loadCartFromLocalStorage(), // Load cart from local storage
    reducers: {
        addProduct(state, action) {
            const { pk, thumbnail, product_title } = action.payload; // Destructure payload
            const existingProduct = state.products.find(product => product.pk === pk);
            if (existingProduct) {
                existingProduct.quantity += 1;
            } else {
                state.products.push({ pk, thumbnail, product_title, quantity: 1 });
            }
            saveCartToLocalStorage(state);
        },
        removeProduct(state, action) {
            const index = state.products.findIndex(product => product.pk === action.payload);
            if (index !== -1) {
                state.products.splice(index, 1);
            }
            saveCartToLocalStorage(state);
        },
        clearCart(state) {
            state.products = [];
            saveCartToLocalStorage(state);
        }
    }
});

export const { addProduct, removeProduct, clearCart } = cartSlice.actions;
export default cartSlice.reducer;
