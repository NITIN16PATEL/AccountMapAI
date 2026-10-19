import { fireEvent, render, screen } from '@testing-library/react';
import App from './App';
import { MemoryRouter } from 'react-router-dom';

describe('App', () => {
  it('renders landing page title', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getAllByRole('link', { name: /Dashboard/i }).length).toBeGreaterThan(0);
  });

  it('shows the floating chat and contact actions', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    expect(screen.getByRole('button', { name: /chat/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /call/i })).toHaveAttribute('href', 'tel:+15551234567');

    fireEvent.click(screen.getByRole('button', { name: /chat/i }));

    expect(screen.getByText(/AccountMap Assistant/i)).toBeInTheDocument();
  });
});
