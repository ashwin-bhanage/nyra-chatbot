import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Send } from 'lucide-react'
import { useCart } from '../context/CartContext'

const InputBox = ({ darkMode, onSend, disabled }) => {
  const [message, setMessage] = useState('')
  const inputRef = useRef(null)
  const { cartCount } = useCart()

  // 🔥 Auto-focus when user types anywhere
  useEffect(() => {
    const handleGlobalKey = (e) => {
      if (disabled) return
      if (document.activeElement === inputRef.current) return

      // Ignore modifier shortcuts
      if (e.metaKey || e.ctrlKey || e.altKey) return

      // Detect any printable key
      if (e.key.length === 1) {
        inputRef.current?.focus()
      }
    }

    window.addEventListener('keydown', handleGlobalKey)
    return () => window.removeEventListener('keydown', handleGlobalKey)
  }, [disabled])

  // Focus when re-enabled
  useEffect(() => {
    if (!disabled && inputRef.current) {
      inputRef.current.focus()
    }
  }, [disabled])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message.trim())
      setMessage('')

      // Re-focus input after sending
      setTimeout(() => inputRef.current?.focus(), 50)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <div
      className={`border-t px-4 py-3 my-2 mx-2 rounded-md ${
        darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
      } ${cartCount > 0 ? 'pb-20 sm:pb-4' : ''}`}
    >
      {/* Input + Send */}
      <form onSubmit={handleSubmit} className="flex items-center gap-3">
        <div className="flex-1">
          <input
            ref={inputRef}
            autoFocus
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

        {/* Send button */}
        <motion.button
          type="submit"
          disabled={!message.trim() || disabled}
          whileHover={message.trim() && !disabled ? { scale: 1.05 } : {}}
          whileTap={message.trim() && !disabled ? { scale: 0.95 } : {}}
          className={`h-12 w-12 flex items-center justify-center rounded-xl ${
            message.trim() && !disabled
              ? 'bg-linear-to-r from-orange-500 to-red-500'
              : darkMode
              ? 'bg-gray-700'
              : 'bg-gray-200'
          } transition-all duration-200 ${
            !message.trim() || disabled ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          <Send
            className={`w-5 h-5 ${
              message.trim() && !disabled
                ? 'text-white'
                : darkMode
                ? 'text-gray-500'
                : 'text-gray-400'
            }`}
          />
        </motion.button>
      </form>

      {/* 🔥 Quick Suggestions */}
      <div className="mt-3 flex flex-wrap gap-2">
        {[
          'Show menu',
          'Order biryani',
          'Book a table',
          'Your hours?',
          'See beverages',
          'Show desserts',
        ].map((suggestion) => (
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
            } ${
              disabled ? 'opacity-50 cursor-not-allowed' : ''
            } transition-all ease-in-out`}
          >
            {suggestion}
          </motion.button>
        ))}
      </div>
    </div>
  )
}

export default InputBox
