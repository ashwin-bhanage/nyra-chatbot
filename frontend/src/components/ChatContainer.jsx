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

  const { addToCartWithQuantity, setIsCartOpen } = useCart()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  // Handle adding items to cart from chat
  const handleCartAction = (cartItems) => {
    console.log('[DEBUG] Adding to cart:', cartItems)

    if (cartItems && cartItems.length > 0) {
      cartItems.forEach(item => {
        // Add item with specified quantity
        addToCartWithQuantity({
          id: item.id,
          name: item.name,
          price: item.price,
          description: item.description || ''
        }, item.quantity)
      })

      // Open cart drawer to show added items
      setTimeout(() => {
        setIsCartOpen(true)
      }, 800)
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

      console.log('[DEBUG] API Response:', response.data)

      // Simulate typing delay
      setTimeout(() => {
        setIsThinking(false)
        setIsTyping(true)
      }, 500)

      // Add bot response with typing animation
      setTimeout(() => {
        const responseData = response.data
        const cartItems = responseData.data?.cart_items || []

        console.log('[DEBUG] Cart items from response:', cartItems)

        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          text: responseData.response,
          intent: responseData.intent,
          action: responseData.action,
          orderId: responseData.order_id,
          reservationId: responseData.reservation_id,
          menuItems: responseData.data?.menu_items || [],
          cartItems: cartItems,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botMessage])
        setIsTyping(false)

        // Handle cart action if items were extracted
        if (cartItems.length > 0) {
          handleCartAction(cartItems)
        }
      }, 1500)

    } catch (error) {
      console.error('[ERROR] Chat error:', error)
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
    <div className="flex-1 flex flex-col overflow-hidden">
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
