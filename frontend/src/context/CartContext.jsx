import { createContext, useContext, useState, useEffect } from 'react'

const CartContext = createContext()

export const useCart = () => {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within CartProvider')
  }
  return context
}

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([])
  const [isCartOpen, setIsCartOpen] = useState(false)

  const addToCart = (item) => {
    setCartItems(prev => {
      const existing = prev.find(i => i.id === item.id)
      if (existing) {
        return prev.map(i =>
          i.id === item.id
            ? { ...i, quantity: i.quantity + 1 }
            : i
        )
      }
      return [...prev, { ...item, quantity: 1 }]
    })
  }

  // Add item with specific quantity (for chat orders)
  const addToCartWithQuantity = (item, quantity) => {
    console.log('[CART] Adding with quantity:', item.name, quantity)
    setCartItems(prev => {
      const existing = prev.find(i => i.id === item.id)
      if (existing) {
        // Add to existing quantity
        return prev.map(i =>
          i.id === item.id
            ? { ...i, quantity: i.quantity + quantity }
            : i
        )
      }
      // New item with specified quantity
      return [...prev, { ...item, quantity: quantity }]
    })
  }

  const removeFromCart = (itemId) => {
    setCartItems(prev => prev.filter(i => i.id !== itemId))
  }

  const updateQuantity = (itemId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(itemId)
      return
    }
    setCartItems(prev =>
      prev.map(i =>
        i.id === itemId
          ? { ...i, quantity }
          : i
      )
    )
  }

  const increaseQuantity = (itemId) => {
    setCartItems(prev =>
      prev.map(i =>
        i.id === itemId
          ? { ...i, quantity: i.quantity + 1 }
          : i
      )
    )
  }

  const decreaseQuantity = (itemId) => {
    setCartItems(prev => {
      const item = prev.find(i => i.id === itemId)
      if (item && item.quantity <= 1) {
        return prev.filter(i => i.id !== itemId)
      }
      return prev.map(i =>
        i.id === itemId
          ? { ...i, quantity: i.quantity - 1 }
          : i
      )
    })
  }

  const clearCart = () => {
    setCartItems([])
  }

  const getItemQuantity = (itemId) => {
    const item = cartItems.find(i => i.id === itemId)
    return item ? item.quantity : 0
  }

  const cartTotal = cartItems.reduce(
    (total, item) => total + (item.price * item.quantity),
    0
  )

  const cartCount = cartItems.reduce(
    (count, item) => count + item.quantity,
    0
  )

  const deliveryFee = cartItems.length > 0 ? 2.99 : 0
  const grandTotal = cartTotal + deliveryFee

  // Debug log
  useEffect(() => {
    console.log('[CART] Current items:', cartItems)
  }, [cartItems])

  return (
    <CartContext.Provider value={{
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
      grandTotal
    }}>
      {children}
    </CartContext.Provider>
  )
}
