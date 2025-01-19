'use client'

import React from 'react';
import { useRouter } from 'next/navigation';

interface ButtonProps {
  buttonText: string;
  path?: string;
}

const Button: React.FC<ButtonProps> = ({ buttonText, path }) => {
  const router = useRouter();
  return (
    <div className="fixed bottom-4 right-4">
      <button className="shadow-[0_0_0_3px_#000000_inset] px-6 py-2 bg-transparent border border-black dark:border-white dark:text-white text-black rounded-lg font-bold transform hover:-translate-y-1 transition duration-400" onClick={() => {
        if(path){
          router.push(`/${path}`)
        }
        }}>
        {buttonText}
      </button>
    </div>
  );
};

export default Button;
