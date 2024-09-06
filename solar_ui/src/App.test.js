import React from 'react';
import { render } from '@testing-library/react';
import App from './App';
import { MemoryRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';  // Correctly import your store

test('renders the app without crashing', () => {
  const { container } = render(
    <Provider store={store}>
      <MemoryRouter>
        <App />
      </MemoryRouter>
    </Provider>
  );
  
  expect(container).toBeInTheDocument();  // Ensure that the app renders something
});
