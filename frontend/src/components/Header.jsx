import { Moon, Sun, Settings, Pizza } from 'lucide-react'
import { motion } from 'framer-motion'

const Header = ({ darkMode, setDarkMode }) => {
  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={`${
        darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
      } border-b px-4 py-3 flex items-center justify-between mx-2 my-2 rounded-md`}
    >
      <div className="flex items-center gap-3">
        <motion.div
          transition={{ duration: 2, ease: "linear" }}
        >
          <Pizza className={`w-8 h-8 ${darkMode ? 'text-purple-400' : 'text-purple-600'}`} />
        </motion.div>
        <div>
          <h1 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Tasty Bites Café
          </h1>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
            Nyra - AI Assistant
          </p>
        </div>
      </div>

      <div className="flex items-center gap-2">
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

export default Header;
