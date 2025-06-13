import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Header from './Header';

describe('Header Component', () => {
  test('renders header with correct title', () => {
    render(<Header />);
    
    expect(screen.getByText('Morse Code Translator')).toBeInTheDocument();
  });

  test('has correct semantic structure', () => {
    render(<Header />);
    
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
    expect(header).toHaveClass('header');
  });

  test('contains proper heading level', () => {
    render(<Header />);
    
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
    expect(heading).toHaveTextContent('Morse Code Translator');
  });


  test('renders consistently', () => {
    const { rerender } = render(<Header />);
    
    expect(screen.getByText('Morse Code Translator')).toBeInTheDocument();
    
    rerender(<Header />);
    
    expect(screen.getByText('Morse Code Translator')).toBeInTheDocument();
  });

  test('accessibility attributes', () => {
    render(<Header />);
    
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
    
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
  });

  test('snapshot consistency', () => {
    const { container } = render(<Header />);
    expect(container.firstChild).toMatchSnapshot();
  });
});
