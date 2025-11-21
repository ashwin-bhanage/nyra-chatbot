import { motion, AnimatePresence } from 'framer-motion'
import { ShoppingCart } from 'lucide-react'
import { useCart } from '../context/CartContext'

const CartFloatingButton = ({ darkMode }) => {
  const { cartCount, setIsCartOpen, grandTotal } = useCart()

  if (cartCount === 0) return null

  return (
    <AnimatePresence>
      <motion.div
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 100, opacity: 0 }}
        className="fixed bottom-24 left-1/2 transform -translate-x-1/2 z-30 sm:hidden"
      >
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setIsCartOpen(true)}
          className="bg-linear-to-r from-purple-600 to-purple-700 text-white px-6 py-3 rounded-full shadow-lg flex items-center gap-3 font-semibold"
        >
          <div className="relative">
            <ShoppingCart className="w-5 h-5" />
            <span className="absolute -top-2 -right-2 bg-white text-purple-600 text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
              {cartCount}
            </span>
          </div>
          <span>View Cart</span>
          <span className="bg-white/20 px-2 py-1 rounded-lg text-sm">
            ₹{grandTotal.toFixed(2)}
          </span>
        </motion.button>
      </motion.div>
    </AnimatePresence>
  )
}

export default CartFloatingButton
