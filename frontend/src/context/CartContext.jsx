import { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext();

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within CartProvider");
  }
  return context;
};

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  // ============================
  // ORDER SUCCESS STATE (NEW)
  // ============================
  const [orderSuccess, setOrderSuccess] = useState(false);
  const [lastOrderId, setLastOrderId] = useState(null);

  const triggerOrderSuccess = (orderId) => {
    setLastOrderId(orderId);
    setOrderSuccess(true);
    clearCart(); // auto-clear cart whenever order completes
  };

  const resetOrderSuccess = () => {
    setOrderSuccess(false);
    setLastOrderId(null);
  };

  // =====================================================
  // VERY IMPORTANT: SYNC CART WITH CHATBOT BACKEND
  // =====================================================
  const setCartFromChatbot = (items) => {
    if (!items || items.length === 0) return;

    setCartItems(
      items.map((i) => ({
        id: i.id,
        name: i.name,
        price: Number(i.price),
        quantity: Number(i.quantity),
        description: i.description || ""
      }))
    );
  };

  // ============================
  // ADD / MERGE ITEM
  // ============================
  const mergeItem = (item, quantity) => {
    setCartItems((prev) => {
      const existing = prev.find((i) => i.id === item.id);

      if (existing) {
        return prev.map((i) =>
          i.id === item.id
            ? { ...i, quantity: i.quantity + quantity }
            : i
        );
      }

      return [...prev, { ...item, quantity }];
    });
  };

  const addToCart = (item) => mergeItem(item, 1);

  const addToCartWithQuantity = (item, quantity) => {
    const q = Number(quantity) || 1;
    mergeItem(item, q);
  };

  // ============================
  // QUANTITY HANDLERS
  // ============================
  const increaseQuantity = (itemId) => {
    setCartItems((prev) =>
      prev.map((i) =>
        i.id === itemId ? { ...i, quantity: i.quantity + 1 } : i
      )
    );
  };

  const decreaseQuantity = (itemId) => {
    setCartItems((prev) => {
      const found = prev.find((i) => i.id === itemId);
      if (found && found.quantity <= 1) {
        return prev.filter((i) => i.id !== itemId);
      }
      return prev.map((i) =>
        i.id === itemId ? { ...i, quantity: i.quantity - 1 } : i
      );
    });
  };

  const updateQuantity = (itemId, quantity) => {
    const q = Number(quantity);
    if (q <= 0) return removeFromCart(itemId);

    setCartItems((prev) =>
      prev.map((i) =>
        i.id === itemId ? { ...i, quantity: q } : i
      )
    );
  };

  // ============================
  // REMOVE ITEMS
  // ============================
  const removeFromCart = (itemId) => {
    setCartItems((prev) => prev.filter((i) => i.id !== itemId));
  };

  const clearCart = () => setCartItems([]);

  // ============================
  // REQUIRED BY MenuItemCard
  // ============================
  const getItemQuantity = (itemId) => {
    const item = cartItems.find(i => i.id === itemId);
    return item ? item.quantity : 0;
  };

  // ============================
  // CART TOTALS
  // ============================
  const cartTotal = cartItems.reduce(
    (total, item) => total + Number(item.price) * Number(item.quantity),
    0
  );

  const cartCount = cartItems.reduce(
    (count, item) => count + item.quantity,
    0
  );

  const deliveryFee = cartItems.length > 0 ? 40 : 0;
  const grandTotal = cartTotal + deliveryFee;

  useEffect(() => {
    console.log("[CART] Items:", cartItems);
  }, [cartItems]);

  return (
    <CartContext.Provider
      value={{
        cartItems,
        isCartOpen,
        setIsCartOpen,

        addToCart,
        addToCartWithQuantity,

        removeFromCart,
        updateQuantity,
        increaseQuantity,
        decreaseQuantity,
        clearCart,
        getItemQuantity,

        cartTotal,
        cartCount,
        deliveryFee,
        grandTotal,

        orderSuccess,
        lastOrderId,
        triggerOrderSuccess,
        resetOrderSuccess,

        // ⭐ NEW FOR CHATBOT SYNC
        setCartFromChatbot
      }}
    >
      {children}
    </CartContext.Provider>
  );
};
