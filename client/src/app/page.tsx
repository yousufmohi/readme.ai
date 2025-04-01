"use client";
import { useState } from "react";
import axios from "axios";
import * as React from "react";
import Navigation from "@/components/ui/Navigations";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"; // Enables GitHub-flavored markdown
import rehypeRaw from "rehype-raw"; // Allows raw HTML inside markdown
import rehypeSanitize from "rehype-sanitize"; // Prevents XSS attacks

export default function Home() {
  const [link, setLink] = useState("");
  const [res, setResult] = useState("");

  const sendLink = async () => {
    try {
      const result = await axios.post("http://127.0.0.1:8000/api/link/", {
        link: link,
      });
      setResult(result.data["data"]); // Ensure API returns valid markdown
    } catch (error) {
      console.error("Error fetching README:", error);
    }
  };

  return (
    <>
      <Navigation />
      <div className="w-full flex items-center mt-20">
        <h1 className="text-6xl font-semibold m-auto my-auto">
          Generate a ReadMe With One Click
        </h1>
      </div>
      <div className="flex w-full max-w-sm items-center space-x-2 mx-auto mt-5">
        <Input
          type="text"
          placeholder="Enter Link"
          onChange={(e) => setLink(e.target.value)}
        />
        <Button type="submit" onClick={sendLink}>
          Get Readme
        </Button>
      </div>

      {/* Markdown Display Section */}
      <div className="prose max-w-2xl mx-auto p-5 bg-gray-100 rounded-lg shadow-md">
      </div>
    </>
  );
}
