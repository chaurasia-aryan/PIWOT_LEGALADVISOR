"use client";
import React, { useState } from "react";
import { HoveredLink, Menu, MenuItem, ProductItem } from "@/ui/navbar-menu";
import { cn } from "@/lib/utils";

export function NavbarFinal() {
  return (
    <div className="relative w-full flex items-center justify-center border-b border-gray-200 dark:border-gray-700">
      <Navbar className="top-2" />
    </div>
  );
}

function Navbar({ className }: { className?: string }) {
  const [active, setActive] = useState<string | null>(null);
  return (
    <div
      className={cn("fixed top-10 inset-x-0 max-w-2xl mx-auto z-50", className)}
    >
      <Menu setActive={setActive}>
        <MenuItem setActive={setActive} active={active} item="Services">
          <div className="flex flex-col space-y-4 text-sm">
            <HoveredLink href="/Services/smart-contract-parsing">Smart Contract Parsing</HoveredLink>
            <HoveredLink href="/Services/summary-generation">Summary Generation</HoveredLink>
            <HoveredLink href="/Services/collaboration-tools">Collaboration Tools</HoveredLink>
            <HoveredLink href="/Services/document-signing">Document-Signing</HoveredLink>
          </div>
        </MenuItem>
        
      </Menu>
    </div>
  );
}
