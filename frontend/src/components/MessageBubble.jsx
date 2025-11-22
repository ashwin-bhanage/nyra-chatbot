import { motion } from "framer-motion";
import {
  Bot,
  User,
  ShoppingCart,
  Calendar,
  CheckCircle,
  Package
} from "lucide-react";
import MenuItemCard from "./MenuItemCard";

const MessageBubble = ({ message, darkMode }) => {
  const isBot = message.type === "bot";

  // Human-readable labels for categories
  const categoryLabels = {
    APPETIZER: "Appetizers",
    MAIN: "Main Course",
    DESSERT: "Desserts",
    BEVERAGE: "Beverages"
  };

  // Group menu items safely
  const groupedMenu =
    Array.isArray(message.menuItems) && message.menuItems.length > 0
      ? message.menuItems.reduce((groups, item) => {
          const rawCat = item.category || "OTHER";
          const label = categoryLabels[rawCat] || rawCat;
          if (!groups[label]) groups[label] = [];
          groups[label].push(item);
          return groups;
        }, {})
      : {};

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className={`flex gap-3 ${isBot ? "justify-start" : "justify-end"}`}
    >
      {/* Bot Icon */}
      {isBot && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 bg-linear-to-r from-orange-500 to-red-500"
        >
          <Bot className="w-5 h-5 text-white" />
        </motion.div>
      )}

      <div className={`max-w-2xl ${isBot ? "" : "flex flex-col items-end"}`}>
        {/* Chat Bubble */}
        <motion.div
          initial={{ scale: 0.85 }}
          animate={{ scale: 1 }}
          className={`px-4 py-3 rounded-2xl shadow-lg ${
            isBot
              ? darkMode
                ? "bg-gray-800 text-gray-100"
                : "bg-white text-gray-900"
              : "bg-linear-to-r from-orange-500 to-red-500 text-white"
          }`}
        >
          {/* Action Badges */}
          {message.action && (
            <div className="mb-2 flex items-center gap-2">
              {message.action === "items_added_to_cart" && (
                <>
                  <ShoppingCart className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-500 font-semibold">
                    Added to Cart!
                  </span>
                </>
              )}

              {message.action === "order_created" && (
                <>
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-500 font-semibold">
                    Order Created!
                  </span>
                </>
              )}

              {message.action === "reservation_created" && (
                <>
                  <CheckCircle className="w-4 h-4 text-blue-500" />
                  <span className="text-sm text-blue-500 font-semibold">
                    Reservation Confirmed!
                  </span>
                </>
              )}
            </div>
          )}

          {/* Main Text */}
          <div className="whitespace-pre-wrap">{message.text}</div>

          {/* Cart Items */}
          {message.cartItems && message.cartItems.length > 0 && (
            <div
              className={`mt-3 pt-3 border-t ${
                darkMode ? "border-gray-700" : "border-gray-200"
              }`}
            >
              <div className="flex items-center gap-2 text-sm mb-2">
                <Package className="w-4 h-4 text-orange-500" />
                <span className="font-semibold">Items in Cart:</span>
              </div>

              {message.cartItems.map((item, idx) => (
                <div key={idx} className="flex justify-between text-sm py-1">
                  <span>
                    {item.quantity}x {item.name}
                  </span>
                  <span className="text-orange-500">
                    ₹{(item.price * item.quantity).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Order ID */}
          {message.orderId && (
            <div
              className={`mt-2 pt-2 border-t ${
                darkMode ? "border-gray-700" : "border-gray-200"
              } text-sm flex items-center gap-2`}
            >
              <ShoppingCart className="w-4 h-4" />
              <span>Order #{message.orderId}</span>
            </div>
          )}

          {/* Reservation ID */}
          {message.reservationId && (
            <div
              className={`mt-2 pt-2 border-t ${
                darkMode ? "border-gray-700" : "border-gray-200"
              } text-sm flex items-center gap-2`}
            >
              <Calendar className="w-4 h-4" />
              <span>Reservation #{message.reservationId}</span>
            </div>
          )}
        </motion.div>

        {/* Grouped Menu Items */}
        {Object.keys(groupedMenu).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-4 w-full space-y-6"
          >
            {Object.entries(groupedMenu).map(([category, items]) => (
              <div key={category}>
                {/* Category Title */}
                <div
                  className={`text-lg font-semibold mb-2 ${
                    darkMode ? "text-orange-400" : "text-orange-600"
                  }`}
                >
                  {category}
                </div>

                {/* Items Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {items.map((item) => (
                    <MenuItemCard key={item.id} item={item} darkMode={darkMode} />
                  ))}
                </div>
              </div>
            ))}
          </motion.div>
        )}

        {/* Timestamp */}
        <div
          className={`text-xs mt-1 ${
            darkMode ? "text-gray-500" : "text-gray-400"
          }`}
        >
          {message.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
          })}
        </div>
      </div>

      {/* User Icon */}
      {!isBot && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
            darkMode ? "bg-gray-700" : "bg-gray-300"
          }`}
        >
          <User
            className={`w-5 h-5 ${
              darkMode ? "text-gray-300" : "text-gray-700"
            }`}
          />
        </motion.div>
      )}
    </motion.div>
  );
};

export default MessageBubble;
