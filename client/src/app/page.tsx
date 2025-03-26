"use client"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [link,setLink] = useState("");

  const sendLink = async() => {
    const result = await axios.post("http://127.0.0.1:8000/api/link/", {
      "link": link
    });
  }

  return (
    <div className="flex w-full max-w-sm items-center space-x-2">
      <Input type="email" placeholder="Enter Link" onChange={(e) => setLink(e.target.value)}/>
      <Button type="submit" onClick={sendLink}>Get Readme</Button>
    </div>
  );
}
