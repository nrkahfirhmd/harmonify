import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Main from './Main';
import Login from './pages/Login';
import Register from './pages/Register';
import reportWebVitals from './reportWebVitals';
import Header from './components/Header';
import Footer from './components/Footer';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div className="px-5 md:px-20 bg-[#F8F4E1] w-full min-h-screen flex flex-col gap-5">
      <Header />
      <Register />
      <Footer />
    </div>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
