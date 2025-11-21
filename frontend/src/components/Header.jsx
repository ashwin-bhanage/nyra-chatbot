import { Moon, Sun, Settings, Pizza, ShoppingCart } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useCart } from '../context/CartContext'

const Header = ({ darkMode, setDarkMode }) => {
  const { cartCount, setIsCartOpen, isCartOpen } = useCart()

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={`${
        darkMode ? 'bg-gray-800 border-gray-700' : 'bg-gray-100 border-gray-200'
      } border-b px-4 py-3 flex items-center justify-between z-40 m-2 rounded-md shadow-md`}
    >
      <div className="flex items-center gap-3">
        <motion.div
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        >
          <Pizza className={`w-8 h-8 ${darkMode ? 'text-purple-400' : 'text-purple-600'}`} />
        </motion.div>
        <div>
          <h1 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Tasty Bites Café
          </h1>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            AI Assistant
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
        {/* Cart Button */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsCartOpen(!isCartOpen)}
          className={`p-2 rounded-lg relative ${
            darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'
          } ${isCartOpen ? 'ring-2 ring-purple-500' : ''}`}
        >
          <ShoppingCart className={`w-5 h-5 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`} />
          <AnimatePresence>
            {cartCount > 0 && (
              <motion.span
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0 }}
                className="absolute -top-2 -right-2 bg-purple-600 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center"
              >
                {cartCount}
              </motion.span>
            )}
          </AnimatePresence>
        </motion.button>

        {/* Theme Toggle */}
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setDarkMode(!darkMode)}
          className={`p-2 rounded-lg ${
            darkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-100 hover:bg-gray-200'
          }`}
        >
          {darkMode ? (
            <Sun className="w-5 h-5 text-yellow-400" />
          ) : (
            <Moon className="w-5 h-5 text-gray-700" />
          )}
        </motion.button>
      </div>
    </motion.header>
  )
}

export default Header
