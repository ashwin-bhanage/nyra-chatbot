import { motion, AnimatePresence } from 'framer-motion'
import { X, ShoppingBag, Trash2, Plus, Minus, ShoppingCart } from 'lucide-react'
import { useCart } from '../context/CartContext'
import axios from 'axios'
import { useState } from 'react'

const CartDrawer = ({ darkMode }) => {
  const {
    cartItems,
    isCartOpen,
    setIsCartOpen,
    increaseQuantity,
    decreaseQuantity,
    removeFromCart,
    clearCart,
    cartTotal,
    cartCount,
    deliveryFee,
    grandTotal
  } = useCart()

  const [isOrdering, setIsOrdering] = useState(false)
  const [orderSuccess, setOrderSuccess] = useState(false)
  const [orderId, setOrderId] = useState(null)

  const handlePlaceOrder = async () => {
    if (cartItems.length === 0) return

    setIsOrdering(true)

    try {
      const orderPayload = {
        phone_number: '+1234567890',
        items: cartItems.map(item => ({
          menu_item_id: item.id,
          quantity: item.quantity
        })),
        delivery_address: '123 Main Street',
        special_instructions: ''
      }

      const response = await axios.post('/api/v1/order', orderPayload)
      setOrderId(response.data.id)
      setOrderSuccess(true)
      clearCart()

      setTimeout(() => {
        setOrderSuccess(false)
        setIsCartOpen(false)
      }, 3000)

    } catch (error) {
      console.error('Order failed:', error)
      alert('Failed to place order. Please try again.')
    } finally {
      setIsOrdering(false)
    }
  }

  return (
    <AnimatePresence>
      {isCartOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsCartOpen(false)}
            className="fixed inset-0 bg-black z-40"
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className={`fixed right-0 top-0 h-full w-full sm:w-96 ${
              darkMode ? 'bg-gray-800' : 'bg-white'
            } shadow-2xl z-50 flex flex-col`}
          >
            {/* Header */}
            <div className={`p-4 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'} flex items-center justify-between`}>
              <div className="flex items-center gap-2">
                <ShoppingBag className={`w-6 h-6 ${darkMode ? 'text-orange-400' : 'text-orange-600'}`} />
                <h2 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                  Your Cart
                </h2>
                {cartCount > 0 && (
                  <span className="bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                    {cartCount} items
                  </span>
                )}
              </div>
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setIsCartOpen(false)}
                className={`p-2 rounded-lg ${darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
              >
                <X className={`w-5 h-5 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`} />
              </motion.button>
            </div>

            {/* Cart Items */}
            <div className="flex-1 overflow-y-auto p-4">
              {orderSuccess ? (
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="flex flex-col items-center justify-center h-full gap-4"
                >
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: 'spring', damping: 10 }}
                    className="w-20 h-20 rounded-full bg-green-500 flex items-center justify-center"
                  >
                    <ShoppingBag className="w-10 h-10 text-white" />
                  </motion.div>
                  <h3 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
                    Order Placed! 🎉
                  </h3>
                  <p className={`text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Your order #{orderId} has been confirmed.<br />
                    We'll start preparing it right away!
                  </p>
                </motion.div>
              ) : cartItems.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full gap-4">
                  <ShoppingCart className={`w-16 h-16 ${darkMode ? 'text-gray-600' : 'text-gray-300'}`} />
                  <p className={`text-center ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                    Your cart is empty.<br />
                    Add some delicious items!
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  <AnimatePresence>
                    {cartItems.map((item) => (
                      <CartItem
                        key={item.id}
                        item={item}
                        darkMode={darkMode}
                        onIncrease={() => increaseQuantity(item.id)}
                        onDecrease={() => decreaseQuantity(item.id)}
                        onRemove={() => removeFromCart(item.id)}
                      />
                    ))}
                  </AnimatePresence>
                </div>
              )}
            </div>

            {/* Footer - Bill Summary */}
            {cartItems.length > 0 && !orderSuccess && (
              <div className={`p-4 border-t ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
                {/* Bill Details */}
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between">
                    <span className={darkMode ? 'text-gray-400' : 'text-gray-600'}>Subtotal</span>
                    <span className={darkMode ? 'text-white' : 'text-gray-900'}>₹{cartTotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className={darkMode ? 'text-gray-400' : 'text-gray-600'}>Delivery Fee</span>
                    <span className={darkMode ? 'text-white' : 'text-gray-900'}>₹{deliveryFee.toFixed(2)}</span>
                  </div>
                  <div className={`flex justify-between pt-2 border-t ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
                    <span className={`font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>Total</span>
                    <span className="font-bold text-orange-500 text-lg">₹{grandTotal.toFixed(2)}</span>
                  </div>
                </div>

                {/* Place Order Button */}
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handlePlaceOrder}
                  disabled={isOrdering}
                  className={`w-full py-4 rounded-xl bg-linear-to-r from-orange-500 to-red-500 text-white font-bold text-lg flex items-center justify-center gap-2 hover:from-orange-600 hover:to-red-600 transition-all ${
                    isOrdering ? 'opacity-75 cursor-not-allowed' : ''
                  }`}
                >
                  {isOrdering ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Placing Order...
                    </>
                  ) : (
                    <>
                      <ShoppingBag className="w-5 h-5" />
                      Place Order (₹{grandTotal.toFixed(2)})
                    </>
                  )}
                </motion.button>
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

// Cart Item Component
const CartItem = ({ item, darkMode, onIncrease, onDecrease, onRemove }) => {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className={`p-3 rounded-xl ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}
    >
      <div className="flex justify-between items-start mb-2">
        <div className="flex-1">
          <h4 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            {item.name}
          </h4>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            ₹{item.price} each
          </p>
        </div>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onRemove}
          className="p-1.5 rounded-lg text-red-500 hover:bg-red-500/10"
        >
          <Trash2 className="w-4 h-4" />
        </motion.button>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onDecrease}
            className={`w-8 h-8 rounded-full flex items-center justify-center ${
              darkMode ? 'bg-gray-600 hover:bg-gray-500' : 'bg-gray-200 hover:bg-gray-300'
            }`}
          >
            <Minus className={`w-4 h-4 ${darkMode ? 'text-white' : 'text-gray-700'}`} />
          </motion.button>

          <motion.span
            key={item.quantity}
            initial={{ scale: 1.3 }}
            animate={{ scale: 1 }}
            className={`w-8 text-center font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}
          >
            {item.quantity}
          </motion.span>

          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onIncrease}
            className="w-8 h-8 rounded-full bg-orange-500 text-white flex items-center justify-center hover:bg-orange-600"
          >
            <Plus className="w-4 h-4" />
          </motion.button>
        </div>

        <span className={`font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          ₹{(item.price * item.quantity).toFixed(2)}
        </span>
      </div>
    </motion.div>
  )
}

export default CartDrawer
