import React from 'react';
import { IoIosPaper } from "react-icons/io";

function Navigation() {
  return (
    <div className='w-full flex shadow-md items-center justify-between max-md:w-full p-4'>
      <h1 className='link text-base-content link-neutral text-xl font-semibold no-underline flex items-center'>
        <IoIosPaper className="mr-2" />  {/* Adds a small margin to the right of the icon */}
        <span className='text-green-500'>readme</span>.ai
      </h1>
    </div>
  );
}

export default Navigation;
