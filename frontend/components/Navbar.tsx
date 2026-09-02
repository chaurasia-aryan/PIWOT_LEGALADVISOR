'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export const Navbar = () => {
  const pathname = usePathname();

  const navLinks = [
    { href: '/', label: 'Overview' },
    { href: '/Dashboard', label: 'Dashboard' },
    { href: '/FileUploader', label: 'Upload' },
    { href: '/AddContract', label: 'Manual Entry' },
  ];

  return (
    <header className="sticky top-0 z-40 w-full bg-canvas/95 backdrop-blur-sm border-b border-hairline transition-colors">
      <div className="max-w-7xl mx-auto px-6 md:px-10 h-18 flex items-center justify-between py-4">
        
        {/* Wordmark with literal backslash glyph */}
        <Link href="/" className="flex items-center gap-2 group">
          <span className="font-sans font-bold text-lg md:text-xl tracking-tight text-ink">
            PIWOT <span className="text-text-secondary font-mono font-normal mx-0.5">\</span> LEGAL ADVISOR
          </span>
          <span className="hidden sm:inline-block font-mono text-[10px] uppercase px-2 py-0.5 rounded bg-surface-secondary text-text-muted border border-surface-warm">
            ML 2.0
          </span>
        </Link>

        {/* Nav Links */}
        <nav className="hidden md:flex items-center space-x-8">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`font-sans text-sm tracking-normal transition-colors ${
                  isActive
                    ? 'text-ink font-semibold'
                    : 'text-text-muted hover:text-ink'
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* CTA Action */}
        <div className="flex items-center gap-3">
          <Link
            href="/Dashboard"
            className="inline-flex items-center justify-center bg-ink text-canvas font-sans text-xs md:text-sm font-medium px-4 py-2 rounded-sm hover:opacity-90 transition-opacity"
          >
            Launch Dashboard
          </Link>
        </div>

      </div>
    </header>
  );
};

export default Navbar;
