'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/dashboard', label: 'Dashboard' },
];

export default function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-20 border-b border-slate-800/60 bg-slate-950/70 backdrop-blur-md">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link href="/" className="text-lg font-semibold text-brand-200">
          🎼 Project Orchestra
        </Link>
        <nav className="flex items-center gap-6 text-sm uppercase tracking-wide text-slate-400">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={pathname === link.href ? 'text-brand-200' : 'hover:text-slate-200'}
            >
              {link.label}
            </Link>
          ))}
          <span className="rounded-full bg-brand-500/70 px-3 py-1 text-xs font-semibold text-slate-950/80">
            Auth coming soon
          </span>
        </nav>
      </div>
    </header>
  );
}
