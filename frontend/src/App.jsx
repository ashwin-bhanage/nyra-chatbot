import { useState } from 'react'
import { CartProvider } from './context/CartContext'
import ChatContainer from './components/ChatContainer'
import Header from './components/Header'
import CartDrawer from './components/CartDrawer'
import CartFloatingButton from './components/CartFloatingButton'

function App() {
  const [darkMode, setDarkMode] = useState(true)

  return (
    <CartProvider>
      <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-200'} transition-colors duration-300`}>
        <div className="max-w-6xl mx-auto h-screen flex flex-col relative">
          <Header darkMode={darkMode} setDarkMode={setDarkMode} />
          <ChatContainer darkMode={darkMode} />
          <CartDrawer darkMode={darkMode} />
          <CartFloatingButton darkMode={darkMode} />
        </div>
      </div>
    </CartProvider>
  )
}

export default App
