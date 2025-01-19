"use client";
import React, { useState } from "react";
import { motion } from "framer-motion";
import Image from "next/image";
import Link from "next/link";
import { IconArrowLeft, IconBrandTabler, IconSettings, IconUserBolt } from "@tabler/icons-react";
import { cn } from "@/lib/utils";

export function SidebarFinal() {

  const homeIcon = "/home-white-icon.png"
  const dashboardIcon = "/dashboard-white-icon.png"
  const chatsIcon = "/messages-white-icon.png"
  const links = [
    {
      label: "Home",
      href: "/FileUploader",
      icon: (
        <Image src={homeIcon} alt="Home-Icon" width={18} height={18}/>
      ),
    },
    {
      label: "Dashboard",
      href: "/Dashboard",
      icon: (
        <Image src={dashboardIcon} alt="Dashboard-Icon" width={18} height={18}/>
      ),
    },
    {
      label: "Messages",
      href: "/Messages",
      icon: (
        <Image src={chatsIcon} alt="Chats-Icon" width={18} height={18} />
      ),
    },
  ];

  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      className={cn(
        "relative h-full flex flex-col bg-gray-100 dark:bg-neutral-800 border-r border-neutral-200 dark:border-neutral-700 transition-all duration-300",
        isHovered ? "w-64" : "w-20"
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Logo Section */}
      <div className="flex items-center justify-center h-20">
        {isHovered ? <Logo /> : <LogoIcon />}
      </div>

      {/* Links Section */}
      <div className="flex-1 flex flex-col items-start px-4">
        {links.map((link, idx) => (
          <Link
            key={idx}
            href={link.href}
            className={cn(
              "flex items-center w-full gap-4 py-3 px-2 rounded-md text-sm text-neutral-700 dark:text-neutral-200 hover:bg-gray-200 dark:hover:bg-neutral-700",
              isHovered ? "justify-start" : "justify-center"
            )}
          >
            {link.icon}
            {isHovered && <span>{link.label}</span>}
          </Link>
        ))}
      </div>

      {/* Footer Section */}
      <div className="p-4">
        <Link
          href="#"
          className="flex items-center gap-4 text-sm text-neutral-700 dark:text-neutral-200 hover:text-black dark:hover:text-white"
        >
          <Image
            src="/home"
            className="h-7 w-7 rounded-full"
            width={50}
            height={50}
            alt="Avatar"
          />
          {isHovered && <span>Manu Arora</span>}
        </Link>
      </div>
    </div>
  );
}

export const Logo = () => {
  return (
    <Link
      href="#"
      className="font-normal flex items-center space-x-2 text-sm text-black dark:text-white"
    >
      <div className="h-5 w-6 bg-black dark:bg-white rounded-lg flex-shrink-0" />
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="font-medium"
      >
        Acet Labs
      </motion.span>
    </Link>
  );
};

export const LogoIcon = () => {
  return (
    <Link
      href="#"
      className="font-normal flex items-center justify-center text-sm text-black dark:text-white"
    >
      <div className="h-5 w-6 bg-black dark:bg-white rounded-lg flex-shrink-0" />
    </Link>
  );
};
