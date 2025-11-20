import { motion } from 'framer-motion'
import { Bot } from 'lucide-react'

const TypingIndicator = ({ darkMode }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      className="flex gap-3"
    >
      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
        darkMode ? 'bg-purple-600' : 'bg-purple-500'
      }`}>
        <Bot className="w-5 h-5 text-white" />
      </div>

      <div className={`px-4 py-3 rounded-2xl ${
        darkMode ? 'bg-gray-800' : 'bg-white'
      } shadow-lg`}>
        <div className="flex gap-1">
          <div className="w-2 h-2 bg-gray-400 rounded-full dot"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full dot"></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full dot"></div>
        </div>
      </div>
    </motion.div>
  )
}

export default TypingIndicator
