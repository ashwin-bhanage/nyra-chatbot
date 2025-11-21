import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send } from 'lucide-react'
import { useCart } from '../context/CartContext'

const InputBox = ({ darkMode, onSend, disabled }) => {
  const [message, setMessage] = useState('')
  const { cartCount } = useCart()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message.trim())
      setMessage('')
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div className={`border-t px-4 py-3 my-2 rounded-md ${
      darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
    } ${cartCount > 0 ? 'pb-20 sm:pb-4' : ''}`}>
      <form onSubmit={handleSubmit} className="flex items-center gap-3">
        {/* Input Field */}
        <div className="flex-1">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={disabled}
            className={`w-full h-12 px-4 rounded-2xl focus:outline-none focus:ring-2 focus:ring-orange-500/50 ${
              darkMode
                ? 'bg-gray-700 text-white placeholder-gray-400'
                : 'bg-gray-100 text-gray-900 placeholder-gray-500'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
          />
        </div>

        {/* Send Button */}
        <motion.button
          type="submit"
          disabled={!message.trim() || disabled}
          whileHover={message.trim() && !disabled ? { scale: 1.05 } : {}}
          whileTap={message.trim() && !disabled ? { scale: 0.95 } : {}}
          className={`h-12 w-12 shrink-0 flex items-center justify-center rounded-xl ${
            message.trim() && !disabled
              ? 'bg-linear-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600'
              : darkMode
              ? 'bg-gray-700'
              : 'bg-gray-200'
          } transition-all duration-200 ${
            !message.trim() || disabled ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          <Send className={`w-5 h-5 ${
            message.trim() && !disabled ? 'text-white' : darkMode ? 'text-gray-500' : 'text-gray-400'
          }`} />
        </motion.button>
      </form>

      {/* Quick Suggestions */}
      <div className="mt-3 flex flex-wrap gap-2">
        {['Show menu', 'Order biryani', 'Book a table', 'Your hours?'].map((suggestion) => (
          <motion.button
            key={suggestion}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => !disabled && onSend(suggestion)}
            disabled={disabled}
            className={`px-3 py-1.5 rounded-full text-sm ${
              darkMode
                ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : ''} transition-all ease-in-out`}
          >
            {suggestion}
          </motion.button>
        ))}
      </div>
    </div>
  )
}

export default InputBox
