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
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const { theme } = useTheme();
  const [link, setLink] = useState("");
  const [markdown, setMarkdown] = useState("");
  const [loading, setLoading] = useState(false);
  const [showReadmeSections, setShowReadmeSections] = useState(false);


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
      {!showReadmeSections && 
            <div className="w-full flex flex-col items-center justify-center text-center mt-24 mb-10 px-4">
            <h1 className="text-5xl lg:text-6xl font-bold max-w-3xl leading-tight">
              Build a Professional <span className="text-green-500">ReadMe</span> in Seconds.
            </h1>
            <p className="text-gray-500 dark:text-gray-400 mt-4 text-lg max-w-xl">
              Paste your GitHub repository link below and generate a polished, clean, and styled README.md instantly.
            </p>
          </div>
      }


      <div className="flex w-full max-w-3xl items-center space-x-4 mx-auto mt-5 mb-5 px-4">
        <Input
          type="text"
          placeholder="https://github.com/your-user/your-repo"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          className="text-lg px-5 py-4 rounded-md border-gray-300"
        />
        <Button
          type="submit"
          onClick={sendLink}
          className="bg-green-500 text-white hover:bg-green-600 px-6 py-3 text-lg font-semibold rounded-md"
          disabled={loading}
        >
          {loading ? "Generating..." : "Get Readme"}
        </Button>
      </div>

      {showReadmeSections && (
        <div className="flex flex-col lg:flex-row gap-6 p-6">
          <div className="w-full lg:w-1/2 h-[700px]">
            <textarea
              className="w-full h-full border border-gray-300 rounded-md p-4 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              value={markdown}
              onChange={(e) => setMarkdown(e.target.value)}
              placeholder="Edit your README markdown here..."
            />
          </div>

          <div className="w-full lg:w-1/2 h-[700px] bg-white border border-gray-200 rounded-xl overflow-y-auto overflow-x-hidden">
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
