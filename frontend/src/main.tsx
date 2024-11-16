import './index.css';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Home } from './pages/Home/Home';
import { Login } from './pages/Login/Login';
import { Create } from './pages/Create/Create';
import { Events } from './pages/Events/Events';
import { EventPage } from './pages/EventPage/EventPage';
import { PayBill } from './pages/PayBill/PayBill';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/create',
    element: <Create />
  },
  {
    path: '/events',
    element: <Events />
  },
  {
    path: '/event/:eventId',
    element: <EventPage />
  },
  {
    path: '/pay/:eventId/:debterId',
    element: <PayBill />
  }
]);

createRoot(document.getElementById('root')!).render(
  <RouterProvider router={router} />
)
