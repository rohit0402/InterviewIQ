import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {Provider} from "react-redux";
import './index.css'
import App from './App.jsx'
import {store} from "./app/store";
import AppInitailizer from "./components/AuthInitializer";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <AppInitailizer>
        <App />
      </AppInitailizer>
    </Provider>
  </StrictMode>,
);