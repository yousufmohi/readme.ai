"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import * as React from "react";
import Navigation from "@/components/ui/Navigations";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSanitize from "rehype-sanitize";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css";
import "github-markdown-css/github-markdown-light.css";
import "@/styles/markdown.css";
import { useTheme } from "next-themes";

export default function Home() {
  const { theme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [link, setLink] = useState("");
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(false);
  const [showReadmeSections, setShowReadmeSections] = useState(false);

  useEffect(() => setMounted(true), []);

  const sendLink = async () => {
    setLoading(true);
    try {
      const result = await axios.post("http://127.0.0.1:8000/api/link/", {
        link: link,
      });
      setMarkdown(result.data["data"]);
      setShowReadmeSections(true);
    } catch (error) {
      console.error("Error fetching README:", error);
      setMarkdown("Failed to generate README. Please check the link or try again.");
    }
    setLoading(false);
  };

  return (
    <>
      <Navigation />
      <div className="w-full flex items-center mt-20">
        <h1 className="text-6xl font-semibold m-auto my-auto text-center px-4">
          Build a Professional <span className="text-green-500">ReadMe</span> in Seconds.
        </h1>
      </div>

      <div className="flex w-full max-w-xl items-center space-x-2 mx-auto mt-5">
        <Input
          type="text"
          placeholder="Enter GitHub repo link"
          value={link}
          onChange={(e) => setLink(e.target.value)}
        />
        <Button type="submit" onClick={sendLink} className="cursor-pointer" disabled={loading}>
          {loading ? "Generating..." : "Get Readme"}
        </Button>
      </div>

      {showReadmeSections && (
        <div className="flex flex-col lg:flex-row gap-6 p-6">
          <div className="w-full lg:w-1/2 h-[600px]">
            <textarea
              className="w-full h-full border border-gray-300 rounded-md p-4 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              value={markdown}
              onChange={(e) => setMarkdown(e.target.value)}
              placeholder="Edit your README markdown here..."
            />
          </div>

          <div className="w-full lg:w-1/2 h-[600px] bg-white border border-gray-200 rounded-xl overflow-y-auto overflow-x-hidden">
            {mounted && (
              <article className={`markdown-body p-6 ${theme === "dark" ? "dark" : ""}`}>
                <Markdown
                  children={markdown}
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw, rehypeSanitize, rehypeHighlight]}
                />
              </article>
            )}
          </div>
        </div>
      )}
    </>
  );
}
