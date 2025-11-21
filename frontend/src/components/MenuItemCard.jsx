import { motion } from 'framer-motion'
import { Plus, Minus, ShoppingCart } from 'lucide-react'
import { useCart } from '../context/CartContext'

const MenuItemCard = ({ item, darkMode }) => {
  const { addToCart, getItemQuantity, increaseQuantity, decreaseQuantity } = useCart()
  const quantity = getItemQuantity(item.id)

  const handleAddToCart = () => {
    addToCart(item)
  }

  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -2 }}
      className={`p-4 rounded-xl ${
        darkMode ? 'bg-gray-700' : 'bg-gray-100'
      } shadow-md`}
    >
      {/* Item Info */}
      <div className="flex justify-between items-start mb-2">
        <h4 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          {item.name}
        </h4>
        <span className="text-lg font-bold text-orange-500">
          ₹{item.price}
        </span>
      </div>

      {item.description && (
        <p className={`text-sm mb-3 line-clamp-2 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          {item.description}
        </p>
      )}

      {/* Add to Cart / Quantity Controls */}
      {quantity === 0 ? (
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleAddToCart}
          className="w-full bg-linear-to-r from-orange-500 to-red-500 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-sm font-medium hover:from-orange-600 hover:to-red-600 transition-all ease-in-out"
        >
          <ShoppingCart className="w-4 h-4" />
          Add to Cart
        </motion.button>
      ) : (
        <div className="flex items-center justify-between">
          <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            ₹{(item.price * quantity).toFixed(2)}
          </span>
          <div className="flex items-center gap-2">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => decreaseQuantity(item.id)}
              className="w-8 h-8 rounded-full bg-orange-500 text-white flex items-center justify-center hover:bg-orange-600 transition-colors"
            >
              <Minus className="w-4 h-4" />
            </motion.button>

            <motion.span
              key={quantity}
              initial={{ scale: 1.3 }}
              animate={{ scale: 1 }}
              className={`w-8 text-center font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}
            >
              {quantity}
            </motion.span>

            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => increaseQuantity(item.id)}
              className="w-8 h-8 rounded-full bg-orange-500 text-white flex items-center justify-center hover:bg-orange-600 transition-colors"
            >
              <Plus className="w-4 h-4" />
            </motion.button>
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default MenuItemCard
