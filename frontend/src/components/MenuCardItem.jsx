import { motion } from 'framer-motion'
import { ShoppingCart } from 'lucide-react'

const MenuItemCard = ({ item, darkMode, }) => {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -2 }}
      className={`p-4 rounded-xl ${
        darkMode ? 'bg-gray-700' : 'bg-gray-100'
      } shadow-md cursor-pointer`}
    >
      <div className="flex justify-between items-start mb-2">
        <h4 className={`font-semibold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          {item.name}
        </h4>
        <span className="text-lg font-bold text-purple-500">
          ₹{item.price}
        </span>
      </div>

      {item.description && (
        <p className={`text-sm mb-3 ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
          {item.description}
        </p>
      )}

      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="w-full bg-linear-to-r from-purple-600 to-purple-700 text-white py-2 px-4 rounded-lg flex items-center justify-center gap-2 text-sm font-medium"
      >
        <ShoppingCart className="w-4 h-4" />
        Order Now
      </motion.button>
    </motion.div>
  )
}

export default MenuItemCard
