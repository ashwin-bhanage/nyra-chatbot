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
        className="fixed bottom-4 left-4 right-4 z-30 sm:hidden"
      >
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={() => setIsCartOpen(true)}
          className="w-full bg-linear-to-r from-orange-500 to-red-500 text-white px-6 py-2 rounded-2xl shadow-2xl flex items-center justify-between font-semibold"
        >
          <div className="flex items-center gap-3">
            <div className="relative">
              <ShoppingCart className="w-6 h-6" />
            </div>
            <div className="text-left">
              <span className="block text-sm opacity-90">{cartCount} items</span>
              <span className="block text-xs opacity-75">View Cart</span>
            </div>
          </div>
          <div className="bg-white/20 px-4 py-2 rounded-xl">
            <span className="text-lg font-bold">${grandTotal.toFixed(2)}</span>
          </div>
        </motion.button>
      </motion.div>
    </AnimatePresence>
  )
}

export default CartFloatingButton
