import { motion } from 'framer-motion'
import { Bot, User, ShoppingCart, Calendar, CheckCircle } from 'lucide-react'
import MenuItemCard from './MenuCardItem'

const MessageBubble = ({ message, darkMode }) => {
  const isBot = message.type === 'bot'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isBot ? 'justify-start' : 'justify-end'}`}
    >
      {isBot && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
            darkMode ? 'bg-purple-600' : 'bg-purple-500'
          }`}
        >
          <Bot className="w-5 h-5 text-white" />
        </motion.div>
      )}

      <div className={`max-w-2xl ${isBot ? '' : 'flex flex-col items-end'}`}>
        {/* Message Content */}
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          className={`px-4 py-3 rounded-2xl shadow-lg ${
            isBot
              ? darkMode
                ? 'bg-gray-800 text-gray-100'
                : 'bg-white text-gray-900'
              : 'bg-linear-to-r from-purple-600 to-purple-700 text-white'
          }`}
        >
          {/* Action Badge */}
          {message.action && (
            <div className="mb-2 flex items-center gap-2">
              {message.action === 'order_created' && (
                <>
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-500 font-semibold">Order Created!</span>
                </>
              )}
              {message.action === 'reservation_created' && (
                <>
                  <CheckCircle className="w-4 h-4 text-blue-500" />
                  <span className="text-sm text-blue-500 font-semibold">Reservation Confirmed!</span>
                </>
              )}
            </div>
          )}

          {/* Message Text */}
          <div className="whitespace-pre-wrap">{message.text}</div>

          {/* Order/Reservation IDs */}
          {message.orderId && (
            <div className="mt-2 pt-2 border-t border-gray-700">
              <div className="flex items-center gap-2 text-sm">
                <ShoppingCart className="w-4 h-4" />
                <span>Order #{message.orderId}</span>
              </div>
            </div>
          )}

          {message.reservationId && (
            <div className="mt-2 pt-2 border-t border-gray-700">
              <div className="flex items-center gap-2 text-sm">
                <Calendar className="w-4 h-4" />
                <span>Reservation #{message.reservationId}</span>
              </div>
            </div>
          )}
        </motion.div>

        {/* Menu Items Grid */}
        {message.menuItems && message.menuItems.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3 w-full"
          >
            {message.menuItems.slice(0, 4).map((item) => (
              <MenuItemCard key={item.id} item={item} darkMode={darkMode} />
            ))}
          </motion.div>
        )}

        {/* Timestamp */}
        <div className={`text-xs mt-1 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>

      {!isBot && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
            darkMode ? 'bg-gray-700' : 'bg-gray-300'
          }`}
        >
          <User className={`w-5 h-5 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`} />
        </motion.div>
      )}
    </motion.div>
  )
}

export default MessageBubble
