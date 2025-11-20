import { useState } from 'react'
import ChatContainer from './components/ChatContainer'
import Header from './components/Header'

function App() {
  const [darkMode, setDarkMode] = useState(true)

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-200'} transition-colors duration-300`}>
      <div className="max-w-6xl mx-auto h-screen flex flex-col">
        <Header darkMode={darkMode} setDarkMode={setDarkMode} />
        <ChatContainer darkMode={darkMode} />
      </div>
    </div>
  )
}

export default App
