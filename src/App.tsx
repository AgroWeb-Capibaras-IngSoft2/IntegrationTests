// src/App.ts
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from 'react-router-dom';

import Catalog from './components/catalog';
import Login from './components/loginservice';
import Registro from './components/registrationservice';
import RegistrationProducts from './components/RegistrationProducts';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/catalog" element={<Catalog />} />
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Registro />} />
        <Route path="/registrar-producto" element={<RegistrationProducts />} />
        {/* otras rutas: */}
      </Routes>
    </Router>
  );
}

export default App;
