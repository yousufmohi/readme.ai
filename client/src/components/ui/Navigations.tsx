import React, {useState, useEffect} from 'react';
import { IoIosPaper } from "react-icons/io";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import {FiSun, FiMoon} from "react-icons/fi";

function Navigation() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);
  
  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <div className='w-full flex shadow-md items-center justify-between max-md:w-full p-4'>
      <h1 className='link text-base-content link-neutral text-xl font-semibold no-underline flex items-center cursor-pointer' onClick={() => window.location.reload()}>
        <IoIosPaper className="mr-2" />
        <span className='text-green-500'>readme</span>.ai
      </h1>
      {mounted && (
        <Button onClick={toggleTheme} className="border-none cursor-pointer" variant="outline" size="sm">
          {theme === "dark" ? <FiMoon /> : <FiSun />}
        </Button>
      )}
    </div>
  );
}

export default Navigation;
