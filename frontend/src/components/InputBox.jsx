import { useState } from "react";
import { motion } from "framer-motion";
import { Send } from "lucide-react";

const InputBox = ({ darkMode, onSend, disabled }) => {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div
      className={`border px-4 py-3 my-2 rounded-md ${
        darkMode ? "bg-gray-800 border-gray-700" : "bg-white border-gray-200"
      }`}
    >
      <form onSubmit={handleSubmit} className="flex items-end gap-3 ">
        <div className="flex flex-1 items-center gap-2">
          <div className="flex flex-1 relative">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={disabled}
              rows={1}
              className={`w-full px-3 py-2.5 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-purple-500 ${
                darkMode
                  ? "bg-gray-700 text-white placeholder-gray-400"
                  : "bg-gray-100 text-gray-900 placeholder-gray-500"
              } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
              style={{ maxHeight: "120px" }}
            />
          </div>

          <div className="button-field flex">
            <motion.button
            type="submit"
            disabled={!message.trim() || disabled}
            whileHover={message.trim() && !disabled ? { scale: 1.05 } : {}}
            whileTap={message.trim() && !disabled ? { scale: 0.95 } : {}}
            className={`px-3 py-2 h-10 rounded-xl ${
              message.trim() && !disabled
                ? "bg-linear-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800"
                : darkMode
                ? "bg-gray-700"
                : "bg-gray-200"
            } transition-all duration-200 ${
              !message.trim() || disabled ? "opacity-50 cursor-not-allowed" : ""
            }`}
          >
            <Send
              className={`w-5 h-5 ${
                message.trim() && !disabled
                  ? "text-white"
                  : darkMode
                  ? "text-gray-500"
                  : "text-gray-400"
              }`}
            />
          </motion.button>
          </div>
        </div>
      </form>

      {/* Quick Suggestions */}
      <div className="mt-3 flex flex-wrap gap-2">
        {["Show menu", "Order pizza", "Book a table", "Your hours?"].map(
          (suggestion) => (
            <motion.button
              key={suggestion}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => !disabled && onSend(suggestion)}
              disabled={disabled}
              className={`px-3 py-1.5 rounded-full text-sm ${
                darkMode
                  ? "bg-gray-700 hover:bg-gray-600 text-gray-300"
                  : "bg-gray-100 hover:bg-gray-200 text-gray-700"
              } ${disabled ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {suggestion}
            </motion.button>
          )
        )}
      </div>
    </div>
  );
};

export default InputBox;
