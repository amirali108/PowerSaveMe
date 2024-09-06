import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import { MemoryRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';  // Correctly import the Redux store

test('renders learn react link', () => {
  render(
    <Provider store={store}>  {/* Use the actual Redux store */}
      <MemoryRouter>
        <App />
      </MemoryRouter>
    </Provider>
  );
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
