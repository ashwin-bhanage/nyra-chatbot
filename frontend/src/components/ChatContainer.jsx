import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import MessageBubble from "./MessageBubble";
import InputBox from "./InputBox";
import TypingIndicator from "./TypingIndicator";
import { useCart } from "../context/CartContext";
import axios from "axios";
import { API_URL } from "../config";

const ChatContainer = ({ darkMode }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: `Hello! Welcome to Royal Spice Kitchen! 👋

I'm your AI assistant. How can I help you today?

I can help you with:
• Browse our delicious menu 🍛
• Place orders 🛒
• Make reservations 📅
• Answer your questions ❓`,
      timestamp: new Date(),
    },
  ]);

  const [isTyping, setIsTyping] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const messagesEndRef = useRef(null);

  const {
    cartItems,
    cartTotal,
    addToCartWithQuantity,
    setIsCartOpen,
    clearCart,
    triggerOrderSuccess,
    orderSuccess,
  } = useCart();

  const [sessionId, setSessionId] = useState(() => `session-${Date.now()}`);

  useEffect(() => {
    if (orderSuccess) {
      setSessionId(`session-${Date.now()}`);
      console.log("[CHAT] Order completed - resetting session");

      setMessages(prev => [
        ...prev,
        {
          id: Date.now(),
          type: "bot",
          text: "🎉 Your order has been placed successfully!\n\nThank you for ordering with us. Your delicious food is being prepared!\n\nWould you like to order something else?",
          timestamp: new Date(),
        }
      ]);
    }
  }, [orderSuccess]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const getCartSummary = () => {
    if (cartItems.length === 0) return "Cart is empty.";
    const items = cartItems.map(item =>
      `${item.quantity}x ${item.name} @ ₹${item.price}`
    ).join(", ");
    return `Current cart: ${items}. Total: ₹${cartTotal}`;
  };

  const isCartRelatedMessage = (text) => {
    const lower = text.toLowerCase();
    const cartKeywords = [
      'cart', 'checkout', 'check out', 'total', 'bill', 'pay', 'payment',
      'confirm', 'place order', 'place my order', 'what did i order',
      'my order', 'summary', 'proceed', 'finalize', 'complete order',
      'view cart', 'show cart', 'see cart', 'what\'s in my cart',
      'ready to order', 'done ordering', 'that\'s all', 'thats all'
    ];
    return cartKeywords.some(kw => lower.includes(kw));
  };

  const handleAddToCart = (items) => {
    if (!items || items.length === 0) return;

    console.log("[CHAT] Adding items to cart:", items);

    items.forEach(item => {
      const price = parseFloat(item.price) || 0;
      const quantity = parseInt(item.quantity) || 1;

      addToCartWithQuantity(
        {
          id: item.id,
          name: item.name,
          price: price,
          description: item.description || ""
        },
        quantity
      );
    });

    // FIX: Force cart open with slight delay
    console.log("[CHAT] Opening cart drawer...");
    setTimeout(() => {
      setIsCartOpen(true);
      console.log("[CHAT] Cart drawer opened");
    }, 500);
  };

  const sendMessage = async (text) => {
    const userMessage = {
      id: Date.now(),
      type: "user",
      text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsThinking(true);

    try {
      let messageToSend = text;
      if (isCartRelatedMessage(text) && cartItems.length > 0) {
        messageToSend = `${text}\n\n[ACTUAL CART: ${getCartSummary()}]`;
      }

      const response = await axios.post(`${API_URL}/api/v1/chat`, {
        message: messageToSend,
        session_id: sessionId,
        phone_number: "+1234567890",
        current_cart: cartItems,
      });

      const data = response.data || {};
      console.log("[CHAT RESPONSE]", data);

      setTimeout(() => {
        setIsThinking(false);
        setIsTyping(true);
      }, 300);

      setTimeout(() => {
        const menuItems = data.menu_items || data.data?.menu_items || [];
        const newCartItems = data.cart_items || data.data?.cart_items || [];

        let responseText = data.response || "I'm not sure how to respond to that.";

        // Show actual cart for cart-related queries
        if (isCartRelatedMessage(text) && cartItems.length > 0 && !newCartItems.length) {
          const itemsList = cartItems.map(item =>
            `• ${item.quantity}x ${item.name} @ ₹${item.price} = ₹${item.price * item.quantity}`
          ).join("\n");

          responseText = `Here's what's in your cart: 🛒\n\n${itemsList}\n\n💰 Subtotal: ₹${cartTotal}\n🚚 Delivery: ₹40\n\n**Total: ₹${cartTotal + 40}**\n\nReady to checkout? Click the cart icon to proceed!`;

          // Also open cart to show them
          setTimeout(() => setIsCartOpen(true), 500);
        }

        // Empty cart message
        if (isCartRelatedMessage(text) && cartItems.length === 0) {
          responseText = "Your cart is empty! 🛒\n\nWould you like to browse our menu? Try saying:\n• 'Show me starters'\n• 'What biryanis do you have?'\n• 'Add 1 Butter Chicken'";
        }

        const botMessage = {
          id: Date.now() + 1,
          type: "bot",
          text: responseText,
          intent: data.intent,
          action: data.action,
          orderId: data.order_id,
          reservationId: data.reservation_id,
          menuItems,
          cartItems: newCartItems,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, botMessage]);
        setIsTyping(false);

        // Only add to cart if NOT a checkout query
        if (newCartItems.length > 0 && !isCartRelatedMessage(text)) {
          handleAddToCart(newCartItems);
        }

        // Order created via chat (not implemented in backend yet)
        if (data.action === "order_created" && data.order_id) {
          triggerOrderSuccess(data.order_id);
          clearCart();
          setIsCartOpen(true);
        }

      }, 1100);

    } catch (error) {
      console.error("[CHAT ERROR]:", error);
      setIsThinking(false);
      setIsTyping(false);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "bot",
          text: "I'm having trouble right now. Please try again.",
          timestamp: new Date(),
        },
      ]);
    }
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div
        className={`flex-1 overflow-y-auto px-4 py-6 space-y-4 mx-2 rounded-lg ${
          darkMode ? "bg-gray-900" : "bg-gray-50"
        }`}
      >
        <AnimatePresence>
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} darkMode={darkMode} />
          ))}
        </AnimatePresence>

        {isThinking && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center"
          >
            <div
              className={`px-4 py-3 rounded-2xl shadow-lg ${
                darkMode ? "bg-gray-800 text-gray-300" : "bg-white text-gray-700"
              }`}
            >
              💭 Thinking...
            </div>
          </motion.div>
        )}

        {isTyping && <TypingIndicator darkMode={darkMode} />}

        <div ref={messagesEndRef} />
      </div>

      <InputBox
        darkMode={darkMode}
        onSend={sendMessage}
        disabled={isTyping || isThinking}
      />
    </div>
  );
};

export default ChatContainer;
