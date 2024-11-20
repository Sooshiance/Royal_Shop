// src/context/cart/cartSlice.js
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

    initialState: loadCartFromLocalStorage(),

    reducers: {
        addProduct(state, action) {
            const newProduct = action.payload;
            const existingProductIndex = state.products.findIndex(product => product.pk === newProduct.pk);

            if (existingProductIndex === -1) {
                state.products.push({ ...newProduct, quantity: 1 });
            } else {
                state.products[existingProductIndex].quantity++;
            }
            saveCartToLocalStorage(state);
        },

        removeProduct(state, action) {
            const productId = action.payload;
            const existingProductIndex = state.products.findIndex(product => product.pk === productId);

            if (existingProductIndex !== -1) {
                if (state.products[existingProductIndex].quantity === 1) {
                    state.products.splice(existingProductIndex, 1);
                } else {
                    state.products[existingProductIndex].quantity--;
                }
            } else {
                console.warn(`Product with id ${productId} not found in cart.`);
            }
            saveCartToLocalStorage(state);
        },

        clearCart(state) {
            state.products = [];
            saveCartToLocalStorage(state);
        },

        updateProductQuantity(state, action) {
            const { productId, quantity } = action.payload;
            const existingProductIndex = state.products.findIndex(product => product.pk === productId);

            if (existingProductIndex !== -1) {
                if (quantity <= 0) {
                    state.products.splice(existingProductIndex, 1);
                } else {
                    state.products[existingProductIndex].quantity = quantity;
                }
            } else {
                console.warn(`Product with id ${productId} not found in cart.`);
            }
            saveCartToLocalStorage(state);
        },
    },
});

export const { addProduct, removeProduct, clearCart, updateProductQuantity } = cartSlice.actions;
export default cartSlice.reducer;
