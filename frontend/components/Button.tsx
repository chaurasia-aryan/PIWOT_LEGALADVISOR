'use client'

import { ButtonHTMLAttributes, forwardRef } from 'react';
import Link from 'next/link';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'tertiary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  href?: string;
  path?: string;
  buttonText?: string;
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  href,
  path,
  buttonText,
  isLoading = false,
  disabled,
  ...props
}, ref) => {
  const baseStyles = 'inline-flex items-center justify-center rounded-sm font-sans font-medium transition-all duration-150 focus:outline-none disabled:opacity-50 disabled:pointer-events-none';
  
  const variants = {
    primary: 'bg-ink text-canvas hover:opacity-90 active:opacity-95',
    secondary: 'bg-canvas text-ink border border-ink hover:bg-surface-secondary',
    tertiary: 'bg-transparent text-ink border border-hairline hover:border-ink',
    danger: 'bg-accent-clay text-canvas hover:opacity-90',
  };

  const sizes = {
    sm: 'px-3.5 py-1.5 text-xs',
    md: 'px-5 py-2.5 text-sm',
    lg: 'px-7 py-3.5 text-base',
  };

  const buttonClasses = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`;
  const targetUrl = href || path;
  const content = children || buttonText;

  if (targetUrl) {
    return (
      <Link href={targetUrl} className={buttonClasses}>
        {isLoading ? (
          <div className="animate-spin rounded-full h-3.5 w-3.5 border-b-2 border-current mr-2" />
        ) : null}
        {content}
      </Link>
    );
  }

  return (
    <button
      ref={ref}
      className={buttonClasses}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="animate-spin rounded-full h-3.5 w-3.5 border-b-2 border-current mr-2" />
      ) : null}
      {children}
    </button>
  );
});

Button.displayName = 'Button';

export default Button;
