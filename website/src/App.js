import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

import { Routes, Route } from "react-router-dom";
import Home from './pages/Home';
import Docs from './pages/Docs';
import Error from './pages/Error';

function App() {
  return (
    <div className="font-poppins App">
      <div id="page-container" className="flex flex-col mx-auto w-full min-h-screen bg-base">
        <main id="page-content" className="flex flex-auto flex-col max-w-full">
          <Navbar />
          <div className="flex flex-auto flex-col w-full">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/docs" element={<Docs />} />
              <Route path="*" element={<Error />} />
            </Routes>
          </div>
          <Footer />
        </main>
      </div>
    </div>
  );
}

export default App;
