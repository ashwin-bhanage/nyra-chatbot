import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import MessageBubble from './MessageBubble'
import InputBox from './InputBox'
import TypingIndicator from './TypingIndicator'
import { useCart } from '../context/CartContext'
import axios from 'axios'

const ChatContainer = ({ darkMode }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: "Hello! Welcome to Royal Spice Kitchen! 👋\n\nI'm your AI assistant. How can I help you today?\n\nI can help you with:\n• Browse our delicious menu 🍛\n• Place orders 🛒\n• Make reservations 📅\n• Answer your questions ❓",
      timestamp: new Date()
    }
  ])
  const [isTyping, setIsTyping] = useState(false)
  const [isThinking, setIsThinking] = useState(false)
  const [sessionId] = useState(() => `session-${Date.now()}`)
  const messagesEndRef = useRef(null)

  const { addToCart, setIsCartOpen } = useCart()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  // Handle adding items to cart from chat
  const handleCartAction = (data) => {
    if (data.cart_items && data.cart_items.length > 0) {
      data.cart_items.forEach(item => {
        // Add each item to cart with specified quantity
        for (let i = 0; i < item.quantity; i++) {
          addToCart({
            id: item.id,
            name: item.name,
            price: item.price,
            description: item.description
          })
        }
      })
      // Open cart drawer to show added items
      setTimeout(() => setIsCartOpen(true), 500)
    }
  }

  const sendMessage = async (text) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])

    // Show thinking indicator
    setIsThinking(true)

    try {
      // Call API
      const response = await axios.post('/api/v1/chat', {
        message: text,
        session_id: sessionId,
        phone_number: '+1234567890'
      })

      // Simulate typing delay
      setTimeout(() => {
        setIsThinking(false)
        setIsTyping(true)
      }, 500)

      // Add bot response with typing animation
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          text: response.data.response,
          intent: response.data.intent,
          action: response.data.action,
          orderId: response.data.order_id,
          reservationId: response.data.reservation_id,
          menuItems: response.data.data?.menu_items || [],
          cartItems: response.data.data?.cart_items || [],
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botMessage])
        setIsTyping(false)

        // Handle cart action if items were added
        if (response.data.data?.cart_items) {
          handleCartAction(response.data.data)
        }
      }, 1500)

    } catch (error) {
      setIsThinking(false)
      setIsTyping(false)

      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden mx-2 rounded-md">
      {/* Messages Area */}
      <div className={`flex-1 overflow-y-auto px-4 py-6 space-y-4 ${
        darkMode ? 'bg-gray-900' : 'bg-gray-50'
      }`}>
        <AnimatePresence>
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              message={message}
              darkMode={darkMode}
            />
          ))}
        </AnimatePresence>

        {isThinking && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-2"
          >
            <div className={`px-4 py-3 rounded-2xl ${
              darkMode ? 'bg-gray-800' : 'bg-white'
            } shadow-lg`}>
              <div className="flex items-center gap-2">
                <span className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                  💭 Thinking
                </span>
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-orange-500 rounded-full thinking-pulse"></div>
                  <div className="w-2 h-2 bg-orange-500 rounded-full thinking-pulse" style={{ animationDelay: '0.3s' }}></div>
                  <div className="w-2 h-2 bg-orange-500 rounded-full thinking-pulse" style={{ animationDelay: '0.6s' }}></div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {isTyping && <TypingIndicator darkMode={darkMode} />}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <InputBox darkMode={darkMode} onSend={sendMessage} disabled={isTyping || isThinking} />
    </div>
  )
}

export default ChatContainer
